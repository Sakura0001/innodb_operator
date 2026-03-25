from __future__ import annotations

import argparse
import csv
import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

import pymysql
import yaml


PREPARE_START = "-- @PREPARE_START"
PREPARE_END = "-- @PREPARE_END"
TIMER_START = "-- @TIMER_START"
TIMER_END = "-- @TIMER_END"


class BenchmarkError(Exception):
    """Base exception for benchmark failures."""


class ConfigError(BenchmarkError):
    """Raised when configuration is invalid."""


class CaseParseError(BenchmarkError):
    """Raised when a SQL case file does not match the expected format."""


@dataclass(frozen=True)
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(frozen=True)
class Settings:
    base_table_name: str
    test_table_name: str
    result_file: str


@dataclass(frozen=True)
class AppConfig:
    db: DBConfig
    settings: Settings
    root_dir: Path


@dataclass(frozen=True)
class ParsedCase:
    path: Path
    description: str
    prepare_statements: tuple[str, ...]
    timer_statements: tuple[str, ...]

    @property
    def ddl_statement(self) -> str:
        return "; ".join(self.timer_statements)


@dataclass(frozen=True)
class ResultRow:
    test_case_name: str
    ddl_statement: str
    execution_time_seconds: str
    timestamp: str


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MySQL InnoDB benchmark SQL cases.")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to the YAML config file. Defaults to config.yaml in the current directory.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--cases",
        help="Comma-separated SQL file names to run, such as case_001.sql,case_002.sql.",
    )
    group.add_argument(
        "--case-range",
        help="Inclusive case index range based on sorted SQL file names, such as 1-10.",
    )
    return parser.parse_args(argv)


def load_config(config_path: Path) -> AppConfig:
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    db_raw = raw.get("db") or {}
    settings_raw = raw.get("settings") or {}

    required_db_keys = ("host", "port", "user", "password", "database")
    missing_db_keys = [key for key in required_db_keys if key not in db_raw]
    if missing_db_keys:
        raise ConfigError(f"Missing db config keys: {', '.join(missing_db_keys)}")

    required_settings_keys = ("base_table_name", "test_table_name", "result_file")
    missing_settings_keys = [key for key in required_settings_keys if key not in settings_raw]
    if missing_settings_keys:
        raise ConfigError(
            f"Missing settings config keys: {', '.join(missing_settings_keys)}"
        )

    db = DBConfig(
        host=str(db_raw["host"]),
        port=int(db_raw["port"]),
        user=str(db_raw["user"]),
        password=str(db_raw["password"]),
        database=str(db_raw["database"]),
    )
    settings = Settings(
        base_table_name=str(settings_raw["base_table_name"]),
        test_table_name=str(settings_raw["test_table_name"]),
        result_file=str(settings_raw["result_file"]),
    )
    return AppConfig(db=db, settings=settings, root_dir=config_path.resolve().parent)


def list_case_paths(test_cases_dir: Path) -> list[Path]:
    if not test_cases_dir.exists():
        raise BenchmarkError(f"Test case directory not found: {test_cases_dir}")
    case_paths = sorted(path for path in test_cases_dir.glob("*.sql") if path.is_file())
    if not case_paths:
        raise BenchmarkError(f"No SQL test cases found in {test_cases_dir}")
    return case_paths


def parse_case_range(raw_range: str, total_cases: int) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)-(\d+)", raw_range.strip())
    if not match:
        raise BenchmarkError(f"Invalid --case-range value: {raw_range}")

    start = int(match.group(1))
    end = int(match.group(2))
    if start < 1 or end < start:
        raise BenchmarkError(f"Invalid --case-range value: {raw_range}")
    if end > total_cases:
        raise BenchmarkError(
            f"Case range {raw_range} exceeds available case count {total_cases}"
        )
    return start, end


def select_case_paths(
    case_paths: Sequence[Path],
    cases_arg: str | None = None,
    case_range_arg: str | None = None,
) -> list[Path]:
    if cases_arg:
        requested_names = [name.strip() for name in cases_arg.split(",") if name.strip()]
        if not requested_names:
            raise BenchmarkError("No case names were provided to --cases")

        lookup = {path.name: path for path in case_paths}
        missing = [name for name in requested_names if name not in lookup]
        if missing:
            raise BenchmarkError(f"Requested case files not found: {', '.join(missing)}")
        return [lookup[name] for name in requested_names]

    if case_range_arg:
        start, end = parse_case_range(case_range_arg, len(case_paths))
        return list(case_paths[start - 1 : end])

    return list(case_paths)


def render_sql_template(sql_text: str, settings: Settings) -> str:
    return (
        sql_text.replace("{{BASE_TABLE_NAME}}", settings.base_table_name)
        .replace("{{TEST_TABLE_NAME}}", settings.test_table_name)
    )


def split_sql_statements(sql_text: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    in_single = False
    in_double = False
    in_backtick = False
    line_comment = False
    block_comment = False
    escaped = False
    index = 0

    while index < len(sql_text):
        char = sql_text[index]
        next_char = sql_text[index + 1] if index + 1 < len(sql_text) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue

        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
                continue
            index += 1
            continue

        if not (in_single or in_double or in_backtick):
            if char == "-" and next_char == "-" and (
                index + 2 >= len(sql_text) or sql_text[index + 2].isspace()
            ):
                line_comment = True
                index += 2
                continue
            if char == "#":
                line_comment = True
                index += 1
                continue
            if char == "/" and next_char == "*":
                block_comment = True
                index += 2
                continue

        if in_single:
            current.append(char)
            if char == "'" and not escaped:
                in_single = False
            escaped = char == "\\" and not escaped
            index += 1
            continue

        if in_double:
            current.append(char)
            if char == '"' and not escaped:
                in_double = False
            escaped = char == "\\" and not escaped
            index += 1
            continue

        if in_backtick:
            current.append(char)
            if char == "`":
                in_backtick = False
            index += 1
            continue

        escaped = False

        if char == "'":
            in_single = True
            current.append(char)
            index += 1
            continue
        if char == '"':
            in_double = True
            current.append(char)
            index += 1
            continue
        if char == "`":
            in_backtick = True
            current.append(char)
            index += 1
            continue
        if char == ";":
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            index += 1
            continue

        current.append(char)
        index += 1

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)

    return statements


def parse_case_file(case_path: Path, settings: Settings) -> ParsedCase:
    rendered_text = render_sql_template(case_path.read_text(encoding="utf-8"), settings)
    description_lines: list[str] = []
    prepare_lines: list[str] = []
    timer_lines: list[str] = []

    section: str | None = None
    seen_prepare_start = False
    seen_prepare_end = False
    seen_timer_start = False
    seen_timer_end = False

    for line_number, raw_line in enumerate(rendered_text.splitlines(), start=1):
        stripped = raw_line.strip()

        if stripped == PREPARE_START:
            if seen_prepare_start or section is not None:
                raise CaseParseError(f"{case_path}:{line_number} invalid PREPARE start marker")
            seen_prepare_start = True
            section = "prepare"
            continue
        if stripped == PREPARE_END:
            if section != "prepare":
                raise CaseParseError(f"{case_path}:{line_number} invalid PREPARE end marker")
            seen_prepare_end = True
            section = None
            continue
        if stripped == TIMER_START:
            if not seen_prepare_start or not seen_prepare_end or section is not None:
                raise CaseParseError(f"{case_path}:{line_number} invalid TIMER start marker")
            seen_timer_start = True
            section = "timer"
            continue
        if stripped == TIMER_END:
            if section != "timer":
                raise CaseParseError(f"{case_path}:{line_number} invalid TIMER end marker")
            seen_timer_end = True
            section = None
            continue

        if stripped.startswith("--"):
            if not seen_prepare_start:
                description_lines.append(stripped[2:].strip())
                continue
            raise CaseParseError(
                f"{case_path}:{line_number} comments are only allowed at the top of the file"
            )

        if not stripped:
            continue

        if section == "prepare":
            prepare_lines.append(raw_line)
            continue
        if section == "timer":
            timer_lines.append(raw_line)
            continue

        raise CaseParseError(
            f"{case_path}:{line_number} SQL content must be inside PREPARE or TIMER markers"
        )

    if not (seen_prepare_start and seen_prepare_end and seen_timer_start and seen_timer_end):
        raise CaseParseError(f"{case_path} is missing required PREPARE/TIMER markers")

    prepare_statements = tuple(split_sql_statements("\n".join(prepare_lines)))
    timer_statements = tuple(split_sql_statements("\n".join(timer_lines)))
    if not timer_statements:
        raise CaseParseError(f"{case_path} does not contain executable TIMER statements")

    return ParsedCase(
        path=case_path,
        description="\n".join(line for line in description_lines if line),
        prepare_statements=prepare_statements,
        timer_statements=timer_statements,
    )


def create_connection(db_config: DBConfig, include_database: bool = True) -> pymysql.Connection:
    connection_kwargs = {
        "host": db_config.host,
        "port": db_config.port,
        "user": db_config.user,
        "password": db_config.password,
        "charset": "utf8mb4",
        "autocommit": True,
    }
    if include_database:
        connection_kwargs["database"] = db_config.database
    return pymysql.connect(**connection_kwargs)


def quote_identifier(identifier: str) -> str:
    return f"`{identifier.replace('`', '``')}`"


def ensure_database_exists(db_config: DBConfig) -> None:
    connection = create_connection(db_config, include_database=False)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {quote_identifier(db_config.database)} "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            )
    finally:
        connection.close()


def execute_statements(connection: pymysql.Connection, statements: Iterable[str]) -> None:
    with connection.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)


def execute_schema(config: AppConfig, schema_path: Path) -> None:
    if not schema_path.exists():
        raise BenchmarkError(f"Schema file not found: {schema_path}")

    rendered_text = render_sql_template(schema_path.read_text(encoding="utf-8"), config.settings)
    statements = split_sql_statements(rendered_text)
    if not statements:
        raise BenchmarkError(f"Schema file does not contain executable SQL: {schema_path}")

    connection = create_connection(config.db)
    try:
        execute_statements(connection, statements)
    finally:
        connection.close()


def execute_case(config: AppConfig, parsed_case: ParsedCase) -> ResultRow:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connection = create_connection(config.db)

    try:
        execute_statements(connection, parsed_case.prepare_statements)
        start = time.perf_counter()
        execute_statements(connection, parsed_case.timer_statements)
        elapsed_seconds = time.perf_counter() - start
        logging.info("Case %s completed in %.6f seconds", parsed_case.path.name, elapsed_seconds)
        execution_value = f"{elapsed_seconds:.6f}"
    except Exception as exc:  # pragma: no cover - exercised by integration run
        logging.exception("Case %s failed", parsed_case.path.name)
        execution_value = f"ERROR: {exc}"
    finally:
        connection.close()

    return ResultRow(
        test_case_name=parsed_case.path.name,
        ddl_statement=parsed_case.ddl_statement,
        execution_time_seconds=execution_value,
        timestamp=timestamp,
    )


def write_results(result_path: Path, results: Sequence[ResultRow]) -> None:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    with result_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ["test_case_name", "ddl_statement", "execution_time_seconds", "timestamp"]
        )
        for row in results:
            writer.writerow(
                [
                    row.test_case_name,
                    row.ddl_statement,
                    row.execution_time_seconds,
                    row.timestamp,
                ]
            )


def run_benchmark(
    config: AppConfig,
    *,
    cases_arg: str | None = None,
    case_range_arg: str | None = None,
) -> Path:
    ensure_database_exists(config.db)

    schema_path = config.root_dir / "schema.sql"
    test_cases_dir = config.root_dir / "test_cases"
    result_path = config.root_dir / config.settings.result_file

    execute_schema(config, schema_path)

    case_paths = list_case_paths(test_cases_dir)
    selected_case_paths = select_case_paths(case_paths, cases_arg=cases_arg, case_range_arg=case_range_arg)
    parsed_cases = [parse_case_file(case_path, config.settings) for case_path in selected_case_paths]
    results = [execute_case(config, parsed_case) for parsed_case in parsed_cases]
    write_results(result_path, results)
    return result_path


def main(argv: Sequence[str] | None = None) -> int:
    configure_logging()

    try:
        args = parse_args(argv)
        config = load_config(Path(args.config))
        result_path = run_benchmark(
            config,
            cases_arg=args.cases,
            case_range_arg=args.case_range,
        )
    except BenchmarkError as exc:
        logging.error(str(exc))
        return 1

    logging.info("Benchmark completed. Results written to %s", result_path)
    return 0
