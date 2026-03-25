from pathlib import Path

from innodb_suanzi.runner import (
    ParsedCase,
    ResultRow,
    Settings,
    parse_case_file,
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

    parsed = parse_case_file(case_path, settings)

    assert isinstance(parsed, ParsedCase)
    assert parsed.prepare_statements == (
        "DROP TABLE IF EXISTS `test_temp`",
        "CREATE TABLE `test_temp` LIKE `test`",
    )
    assert parsed.timer_statements == (
        "ALTER TABLE `test_temp` ADD INDEX `idx_varchar` (`varchar_col`)",
    )
    assert parsed.ddl_statement == "ALTER TABLE `test_temp` ADD INDEX `idx_varchar` (`varchar_col`)"


def test_select_case_paths_and_write_results(tmp_path: Path) -> None:
    case_dir = tmp_path / "test_cases"
    case_dir.mkdir()
    case_paths = []
    for name in ("case_001.sql", "case_002.sql", "case_003.sql"):
        path = case_dir / name
        path.write_text("SELECT 1;", encoding="utf-8")
        case_paths.append(path)

    selected_by_name = select_case_paths(case_paths, cases_arg="case_003.sql,case_001.sql")
    selected_by_range = select_case_paths(case_paths, case_range_arg="1-2")

    assert [path.name for path in selected_by_name] == ["case_003.sql", "case_001.sql"]
    assert [path.name for path in selected_by_range] == ["case_001.sql", "case_002.sql"]

    result_path = tmp_path / "results" / "results.csv"
    write_results(
        result_path,
        [
            ResultRow(
                test_case_name="case_002.sql",
                ddl_statement="ALTER TABLE test_temp DROP COLUMN missing_col",
                execution_time_seconds="ERROR: Unknown column 'missing_col' in 'test_temp'",
                timestamp="2026-03-25 10:00:00",
            )
        ],
    )

    assert result_path.read_text(encoding="utf-8").splitlines() == [
        "test_case_name,ddl_statement,execution_time_seconds,timestamp",
        "case_002.sql,ALTER TABLE test_temp DROP COLUMN missing_col,ERROR: Unknown column 'missing_col' in 'test_temp',2026-03-25 10:00:00",
    ]
