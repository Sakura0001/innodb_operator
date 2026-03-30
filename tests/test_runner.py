from pathlib import Path

import pytest

from innodb_suanzi.runner import (
    AppConfig,
    BenchmarkError,
    DBConfig,
    ParsedCase,
    ResultRow,
    Settings,
    filter_case_paths_by_operation,
    list_case_paths,
    parse_case_file,
    run_benchmark,
    select_case_paths,
    write_results,
)


def test_parse_case_file_extracts_prepare_and_timer_sections(tmp_path: Path) -> None:
    case_path = tmp_path / "case.sql"
    case_path.write_text(
        "\n".join(
            [
                "-- ALTER TABLE {{TEST_TABLE_NAME}} ADD INDEX idx_varchar(varchar_col);",
                "-- 说明文字",
                "",
                "-- @PREPARE_START",
                "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;",
                "CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;",
                "-- @PREPARE_END",
                "",
                "-- @TIMER_START",
                "ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_varchar` (`varchar_col`);",
                "-- @TIMER_END",
            ]
        ),
        encoding="utf-8",
    )
    settings = Settings(
        base_table_name="test",
        test_table_name="test_temp",
        result_file="results/results.csv",
    )

    parsed = parse_case_file(
        case_path,
        settings,
        case_name="alter_add_index/dstore_test_case_001.sql",
    )

    assert isinstance(parsed, ParsedCase)
    assert parsed.case_name == "alter_add_index/dstore_test_case_001.sql"
    assert parsed.prepare_statements == (
        "DROP TABLE IF EXISTS `test_temp`",
        "CREATE TABLE `test_temp` LIKE `test`",
    )
    assert parsed.timer_statements == (
        "ALTER TABLE `test_temp` ADD INDEX `idx_varchar` (`varchar_col`)",
    )
    assert parsed.ddl_statement == "ALTER TABLE `test_temp` ADD INDEX `idx_varchar` (`varchar_col`)"


def test_case_selection_supports_nested_paths_and_operation_filter(tmp_path: Path) -> None:
    case_dir = tmp_path / "test_cases"
    (case_dir / "alter_add_index").mkdir(parents=True)
    (case_dir / "create_index").mkdir(parents=True)

    case_a = case_dir / "alter_add_index" / "dstore_test_case_001.sql"
    case_b = case_dir / "alter_add_index" / "dstore_test_case_002.sql"
    case_c = case_dir / "create_index" / "dstore_test_case_001.sql"
    for path in (case_a, case_b, case_c):
        path.write_text("SELECT 1;", encoding="utf-8")

    all_case_paths = list_case_paths(case_dir)
    assert [path.relative_to(case_dir).as_posix() for path in all_case_paths] == [
        "alter_add_index/dstore_test_case_001.sql",
        "alter_add_index/dstore_test_case_002.sql",
        "create_index/dstore_test_case_001.sql",
    ]

    filtered_paths = filter_case_paths_by_operation(
        all_case_paths,
        case_dir,
        operation="alter_add_index",
    )
    assert [path.relative_to(case_dir).as_posix() for path in filtered_paths] == [
        "alter_add_index/dstore_test_case_001.sql",
        "alter_add_index/dstore_test_case_002.sql",
    ]

    selected_by_name = select_case_paths(
        filtered_paths,
        case_dir,
        cases_arg="dstore_test_case_002.sql",
    )
    selected_by_relative_path = select_case_paths(
        all_case_paths,
        case_dir,
        cases_arg="create_index/dstore_test_case_001.sql",
    )
    selected_by_range = select_case_paths(
        all_case_paths,
        case_dir,
        case_range_arg="2-3",
    )

    assert [path.relative_to(case_dir).as_posix() for path in selected_by_name] == [
        "alter_add_index/dstore_test_case_002.sql",
    ]
    assert [path.relative_to(case_dir).as_posix() for path in selected_by_relative_path] == [
        "create_index/dstore_test_case_001.sql",
    ]
    assert [path.relative_to(case_dir).as_posix() for path in selected_by_range] == [
        "alter_add_index/dstore_test_case_002.sql",
        "create_index/dstore_test_case_001.sql",
    ]

    with pytest.raises(BenchmarkError, match="ambiguous"):
        select_case_paths(all_case_paths, case_dir, cases_arg="dstore_test_case_001.sql")


def test_write_results_uses_relative_case_name(tmp_path: Path) -> None:
    result_path = tmp_path / "results" / "results.csv"
    write_results(
        result_path,
        [
            ResultRow(
                test_case_name="alter_drop_index/dstore_test_case_002.sql",
                ddl_statement="ALTER TABLE test_temp DROP INDEX idx_missing",
                execution_time_seconds="ERROR: Can't DROP 'idx_missing'; check that column/key exists",
                timestamp="2026-03-25 10:00:00",
            )
        ],
    )

    assert result_path.read_text(encoding="utf-8").splitlines() == [
        "test_case_name,ddl_statement,execution_time_seconds,timestamp",
        "alter_drop_index/dstore_test_case_002.sql,ALTER TABLE test_temp DROP INDEX idx_missing,ERROR: Can't DROP 'idx_missing'; check that column/key exists,2026-03-25 10:00:00",
    ]


def test_run_benchmark_executes_schema_and_operation_filter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root_dir = tmp_path
    schema_path = root_dir / "schema.sql"
    schema_path.write_text("CREATE TABLE `{{BASE_TABLE_NAME}}` (`id` int);", encoding="utf-8")

    selected_dir = root_dir / "test_cases" / "alter_add_index"
    other_dir = root_dir / "test_cases" / "create_index"
    selected_dir.mkdir(parents=True)
    other_dir.mkdir(parents=True)
    selected_case = selected_dir / "dstore_test_case_001.sql"
    other_case = other_dir / "dstore_test_case_001.sql"
    for path in (selected_case, other_case):
        path.write_text(
            "\n".join(
                [
                    "-- SELECT 1;",
                    "-- smoke test",
                    "-- @PREPARE_START",
                    "SELECT 1;",
                    "-- @PREPARE_END",
                    "-- @TIMER_START",
                    "SELECT 1;",
                    "-- @TIMER_END",
                ]
            ),
            encoding="utf-8",
        )

    config = AppConfig(
        db=DBConfig(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="password",
            database="test",
        ),
        settings=Settings(
            base_table_name="test",
            test_table_name="test_temp",
            result_file="results/results.csv",
        ),
        root_dir=root_dir,
    )

    calls: list[str] = []
    captured_results: list[ResultRow] = []

    monkeypatch.setattr(
        "innodb_suanzi.runner.ensure_database_exists",
        lambda db_config: calls.append(f"ensure_database:{db_config.database}"),
    )

    def fake_execute_schema(config: AppConfig, schema_path: Path) -> None:
        calls.append(f"schema:{schema_path.name}")

    def fake_execute_case(config: AppConfig, parsed_case: ParsedCase) -> ResultRow:
        calls.append(f"case:{parsed_case.case_name}")
        return ResultRow(
            test_case_name=parsed_case.case_name,
            ddl_statement=parsed_case.ddl_statement,
            execution_time_seconds="0.100000",
            timestamp="2026-03-27 12:00:00",
        )

    def fake_write_results(result_path: Path, results: list[ResultRow]) -> None:
        calls.append(f"write:{result_path.as_posix()}")
        captured_results.extend(results)

    monkeypatch.setattr("innodb_suanzi.runner.execute_schema", fake_execute_schema)
    monkeypatch.setattr("innodb_suanzi.runner.execute_case", fake_execute_case)
    monkeypatch.setattr("innodb_suanzi.runner.write_results", fake_write_results)

    result_path = run_benchmark(config, operation="alter_add_index")

    assert result_path == root_dir / "results" / "results.csv"
    assert calls == [
        "ensure_database:test",
        "schema:schema.sql",
        "case:alter_add_index/dstore_test_case_001.sql",
        f"write:{(root_dir / 'results' / 'results.csv').as_posix()}",
    ]
    assert [row.test_case_name for row in captured_results] == [
        "alter_add_index/dstore_test_case_001.sql",
    ]


def test_parse_generated_insert_select_case() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    case_path = repo_root / "test_cases" / "insert_single_index" / "dstore_test_case_001.sql"
    if not case_path.is_file():
        pytest.skip("run scripts/gen_missing_test_cases.py to generate insert_* cases")
    settings = Settings(
        base_table_name="test",
        test_table_name="test_temp",
        result_file="results/results.csv",
    )
    name = "insert_single_index/dstore_test_case_001.sql"
    parsed = parse_case_file(case_path, settings, case_name=name)
    assert parsed.case_name == name
    assert any("INSERT INTO" in stmt.upper() for stmt in parsed.timer_statements)
    assert any("_src" in stmt for stmt in parsed.prepare_statements)
