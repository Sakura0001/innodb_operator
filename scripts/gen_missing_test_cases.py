#!/usr/bin/env python3
"""Generate benchmark SQL cases for DDL features missing from test_cases/."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "test_cases"


def tpl(
    desc: str,
    timer: str,
    prepare_extra: tuple[str, ...] = (),
    prepare_tail: tuple[str, ...] = (),
) -> str:
    lines = [
        f"-- {timer}",
        f"-- {desc}",
        "",
        "-- @PREPARE_START",
        "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;",
    ]
    lines.extend(prepare_extra)
    lines.extend(
        [
            "CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;",
        ]
    )
    lines.extend(prepare_tail)
    lines.extend(
        [
            "-- @PREPARE_END",
            "",
            "-- @TIMER_START",
            timer,
            "-- @TIMER_END",
            "",
        ]
    )
    return "\n".join(lines)


def write_many(
    op: str,
    items: list[tuple],
) -> None:
    d = OUT / op
    d.mkdir(parents=True, exist_ok=True)
    for i, row in enumerate(items, start=1):
        if len(row) == 2:
            desc, timer = row
            extra, tail = (), ()
        elif len(row) == 3:
            desc, timer, extra = row
            tail = ()
        else:
            desc, timer, extra, tail = row
        p = d / f"dstore_test_case_{i:03d}.sql"
        p.write_text(tpl(desc, timer, extra, tail), encoding="utf-8")


def item(desc: str, timer: str, extra: tuple[str, ...] = (), tail: tuple[str, ...] = ()) -> tuple:
    return (desc, timer, extra, tail)


# --- DML INSERT: B = {{TEST_TABLE_NAME}}, C = {{TEST_TABLE_NAME}}_src, A = {{BASE_TABLE_NAME}} ---

EXTRA_DROP_INSERT_SRC = ("DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_src`;",)

_DIGITS_10 = (
    "(SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 "
    "UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9)"
)


def _sql_nums_0_99999() -> str:
    d = _DIGITS_10
    return f"""SELECT a.N + b.N * 10 + c.N * 100 + d.N * 1000 + e.N * 10000 AS n
FROM {d} a, {d} b, {d} c, {d} d, {d} e"""


_INSERT_COL_LIST = (
    "`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, "
    "`smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, "
    "`datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, "
    "`tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, "
    "`mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, "
    "`unsigned_decimal_col`"
)

_INSERT_SELECT_LIST = (
    "{id} AS `id_col`, s.`int_col`, s.`bigint_col`, s.`year_col`, s.`char_col`, s.`tinyint_col`, "
    "s.`bool_col`, s.`smallint_col`, s.`mediumint_col`, s.`decimal_col`, s.`float_col`, s.`double_col`, "
    "s.`date_col`, s.`datetime_col`, s.`timestamp_col`, s.`time_col`, {vc} AS `varchar_col`, "
    "s.`binary_col`, s.`varbinary_col`, s.`tinyblob_col`, s.`blob_col`, s.`mediumblob_col`, "
    "s.`longblob_col`, s.`tinytext_col`, s.`text_col`, s.`mediumtext_col`, s.`longtext_col`, "
    "s.`enum_col`, s.`set_col`, s.`bit_col`, {ui} AS `unsigned_int_col`, s.`unsigned_decimal_col`"
)


def sql_fill_src(
    n_rows: int,
    id_start: int,
    *,
    varchar_sel: str | None = None,
    uint_sel: str | None = None,
) -> str:
    vc = varchar_sel or "s.`varchar_col`"
    ui = uint_sel or "s.`unsigned_int_col`"
    id_expr = f"{id_start} + nums.n"
    sel = _INSERT_SELECT_LIST.format(id=id_expr, vc=vc, ui=ui)
    nums = _sql_nums_0_99999()
    return f"""INSERT INTO `{{{{TEST_TABLE_NAME}}}}_src` ({_INSERT_COL_LIST})
SELECT {sel}
FROM (SELECT * FROM `{{{{BASE_TABLE_NAME}}}}` LIMIT 1) s
CROSS JOIN ({nums}) nums
WHERE nums.n < {n_rows}"""


def insert_prepare_tail(
    index_stmts: tuple[str, ...],
    n_rows: int,
    id_start: int,
    *,
    pre_index: tuple[str, ...] = (),
    varchar_sel: str | None = None,
    uint_sel: str | None = None,
) -> tuple[str, ...]:
    head = pre_index + index_stmts
    fill = sql_fill_src(n_rows, id_start, varchar_sel=varchar_sel, uint_sel=uint_sel)
    return head + (
        "CREATE TABLE `{{TEST_TABLE_NAME}}_src` LIKE `{{BASE_TABLE_NAME}}`;",
        fill,
    )


_TIMER_INSERT_STAR = "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src`;"
_TIMER_INSERT_EXPLICIT = (
    "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, "
    "`bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, "
    "`datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, "
    "`tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, "
    "`mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, "
    "`unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, "
    "`bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, "
    "`datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, "
    "`tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, "
    "`mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, "
    "`unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src`;"
)


def write_dml_insert_cases() -> None:
    idx_single = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_insert_single_int` (`int_col`);",)
    idx_desc = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_insert_desc_vc` (`varchar_col` DESC);",)
    idx_comp = (
        "ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_insert_comp` (`year_col`, `int_col`, `varchar_col`(16));",
    )
    idx_prefix = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_insert_prefix` (`varchar_col`(32));",)
    idx_expr = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_insert_expr` ((ABS(`bigint_col`)));",)
    pre_uq = (
        "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('b_', `id_col`) WHERE 1=1;",
    )
    idx_unique = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_insert_uq_vc` (`varchar_col`);",)
    vc_unique = "CONCAT('c_', LPAD(nums.n, 10, '0'))"

    sizes = ((10000, "1万"), (50000, "5万"), (100000, "10万"))

    def pack(desc: str, timer: str, idx: tuple[str, ...], n: int, id_start: int, **kw) -> tuple:
        return item(desc, timer, EXTRA_DROP_INSERT_SRC, insert_prepare_tail(idx, n, id_start, **kw))

    # insert_single_index: 20 cases — 3 sizes × variants + extras
    single: list[tuple] = []
    bid = 11_000_000
    for n, lab in sizes:
        single.append(
            pack(
                f"测试单列索引 int_col 下从 C 插入{lab}行 INSERT SELECT * 的执行情况",
                _TIMER_INSERT_STAR,
                idx_single,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        single.append(
            pack(
                f"测试单列索引 int_col 下从 C 插入{lab}行 INSERT SELECT * ORDER BY id_col 的执行情况",
                "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `id_col`;",
                idx_single,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        single.append(
            pack(
                f"测试单列索引 int_col 下从 C 插入{lab}行显式列列表 INSERT 的执行情况",
                _TIMER_INSERT_EXPLICIT,
                idx_single,
                n,
                bid,
            )
        )
        bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入1万行 WHERE int_col IS NOT NULL 过滤 INSERT 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `int_col` IS NOT NULL;",
            idx_single,
            10000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入5万行 ORDER BY int_col,year_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `int_col`, `year_col`;",
            idx_single,
            50000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 派生子查询插入5万行的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 0) AS t;",
            idx_single,
            50000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入10万行 WHERE id_col 偶数 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 0;",
            idx_single,
            100000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入1万行 ORDER BY year_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `year_col`;",
            idx_single,
            10000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入5万行 WHERE enum_col='aaa' 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `enum_col` = 'aaa';",
            idx_single,
            50000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入10万行 ORDER BY varchar_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col`;",
            idx_single,
            100000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入1万行显式列 WHERE id_col 模3 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 3 = 0;",
            idx_single,
            10000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入5万行 ORDER BY datetime_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `datetime_col`;",
            idx_single,
            50000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入10万行 WHERE smallint_col IS NOT NULL 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `smallint_col` IS NOT NULL;",
            idx_single,
            100000,
            bid,
        )
    )
    bid += 400_000
    single.append(
        pack(
            "测试单列索引 int_col 下从 C 插入1万行 ORDER BY float_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `float_col`;",
            idx_single,
            10000,
            bid,
        )
    )
    assert len(single) == 20
    write_many("insert_single_index", single)

    # insert_desc_index
    desc_cases: list[tuple] = []
    bid = 12_000_000
    for n, lab in sizes:
        desc_cases.append(
            pack(
                f"测试逆序索引 varchar_col DESC 下从 C 插入{lab}行 INSERT SELECT * 的执行情况",
                _TIMER_INSERT_STAR,
                idx_desc,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        desc_cases.append(
            pack(
                f"测试逆序索引 varchar_col DESC 下从 C 插入{lab}行 ORDER BY varchar_col DESC 的执行情况",
                "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col` DESC;",
                idx_desc,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        desc_cases.append(
            pack(
                f"测试逆序索引 varchar_col DESC 下从 C 插入{lab}行显式列 INSERT 的执行情况",
                _TIMER_INSERT_EXPLICIT,
                idx_desc,
                n,
                bid,
            )
        )
        bid += 400_000
    for label, wh in (
        ("WHERE varchar_col IS NOT NULL", "`varchar_col` IS NOT NULL"),
        ("WHERE id_col 模3", "`id_col` % 3 = 0"),
        ("ORDER BY id_col 与索引列交互", None),
    ):
        if wh:
            tmr = f"INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE {wh};"
        else:
            tmr = "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `id_col`;"
        desc_cases.append(
            pack(
                f"测试逆序索引 varchar_col DESC 下从 C 插入1万行{label}的执行情况",
                tmr,
                idx_desc,
                10000,
                bid,
            )
        )
        bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入5万行 ORDER BY bigint_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `bigint_col`;",
            idx_desc,
            50000,
            bid,
        )
    )
    bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入10万行显式列且 ORDER BY year_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `year_col`;",
            idx_desc,
            100000,
            bid,
        )
    )
    bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入5万行 ORDER BY varchar_col ASC 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col` ASC;",
            idx_desc,
            50000,
            bid,
        )
    )
    bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入1万行 WHERE varchar_col LIKE c_% 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `varchar_col` LIKE 'c_%';",
            idx_desc,
            10000,
            bid,
        )
    )
    bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入10万行 WHERE int_col BETWEEN -50000 AND 50000 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `int_col` BETWEEN -50000 AND 50000;",
            idx_desc,
            100000,
            bid,
        )
    )
    bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入1万行派生表 LIMIT 5000 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` LIMIT 5000) t;",
            idx_desc,
            10000,
            bid,
        )
    )
    bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入5万行 ORDER BY unsigned_int_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `unsigned_int_col`;",
            idx_desc,
            50000,
            bid,
        )
    )
    bid += 400_000
    desc_cases.append(
        pack(
            "测试逆序索引 varchar_col DESC 下从 C 插入10万行 ORDER BY decimal_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `decimal_col`;",
            idx_desc,
            100000,
            bid,
        )
    )
    assert len(desc_cases) == 20
    write_many("insert_desc_index", desc_cases)

    # insert_composite_index
    comp: list[tuple] = []
    bid = 13_000_000
    for n, lab in sizes:
        comp.append(
            pack(
                f"测试组合索引 year_col+int_col+varchar(16) 下从 C 插入{lab}行 INSERT SELECT * 的执行情况",
                _TIMER_INSERT_STAR,
                idx_comp,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        comp.append(
            pack(
                f"测试组合索引下从 C 插入{lab}行 ORDER BY year_col,int_col 的执行情况",
                "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `year_col`, `int_col`;",
                idx_comp,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        comp.append(
            pack(
                f"测试组合索引下从 C 插入{lab}行显式列 INSERT 的执行情况",
                _TIMER_INSERT_EXPLICIT,
                idx_comp,
                n,
                bid,
            )
        )
        bid += 400_000
    for label, tmr in (
        ("WHERE year_col IS NOT NULL", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `year_col` IS NOT NULL;"),
        ("WHERE int_col 模2", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `int_col` % 2 = 0;"),
        ("部分索引列过滤 varchar", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `varchar_col` LIKE 'c_%' OR `varchar_col` IS NOT NULL;"),
        ("ORDER BY 索引首列 year_col", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `year_col` DESC;"),
        ("派生表半量插入", ""),
    ):
        if "派生表" in label:
            comp.append(
                pack(
                    f"测试组合索引下从 C 插入5万行{label}的执行情况",
                    "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 0) t;",
                    idx_comp,
                    50000,
                    bid,
                )
            )
        else:
            comp.append(
                pack(
                    f"测试组合索引下从 C 插入1万行{label}的执行情况",
                    tmr,
                    idx_comp,
                    10000,
                    bid,
                )
            )
        bid += 400_000
    comp.append(
        pack(
            "测试组合索引下从 C 插入5万行 ORDER BY varchar_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col`;",
            idx_comp,
            50000,
            bid,
        )
    )
    bid += 400_000
    comp.append(
        pack(
            "测试组合索引下从 C 插入10万行 WHERE enum_col='aaa' 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `enum_col` = 'aaa';",
            idx_comp,
            100000,
            bid,
        )
    )
    bid += 400_000
    comp.append(
        pack(
            "测试组合索引下从 C 插入1万行显式列 ORDER BY int_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `int_col`;",
            idx_comp,
            10000,
            bid,
        )
    )
    bid += 400_000
    comp.append(
        pack(
            "测试组合索引下从 C 插入5万行 ORDER BY decimal_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `decimal_col`;",
            idx_comp,
            50000,
            bid,
        )
    )
    bid += 400_000
    comp.append(
        pack(
            "测试组合索引下从 C 插入10万行 WHERE set_col IS NOT NULL 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `set_col` IS NOT NULL;",
            idx_comp,
            100000,
            bid,
        )
    )
    bid += 400_000
    comp.append(
        pack(
            "测试组合索引下从 C 插入1万行 ORDER BY unsigned_decimal_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `unsigned_decimal_col`;",
            idx_comp,
            10000,
            bid,
        )
    )
    bid += 400_000
    assert len(comp) == 20
    write_many("insert_composite_index", comp)

    # insert_prefix_index
    pref: list[tuple] = []
    bid = 14_000_000
    for n, lab in sizes:
        pref.append(
            pack(
                f"测试前缀索引 varchar_col(32) 下从 C 插入{lab}行 INSERT SELECT * 的执行情况",
                _TIMER_INSERT_STAR,
                idx_prefix,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        pref.append(
            pack(
                f"测试前缀索引下从 C 插入{lab}行 ORDER BY varchar_col 的执行情况",
                "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col`;",
                idx_prefix,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        pref.append(
            pack(
                f"测试前缀索引下从 C 插入{lab}行显式列 INSERT 的执行情况",
                _TIMER_INSERT_EXPLICIT,
                idx_prefix,
                n,
                bid,
            )
        )
        bid += 400_000
    for label, tmr in (
        ("WHERE LENGTH(varchar_col)>0", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE CHAR_LENGTH(`varchar_col`) > 0;"),
        ("非索引列过滤 date_col", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `date_col` IS NOT NULL;"),
        ("ORDER BY id_col", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `id_col`;"),
        ("偶数 id 过滤", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 1;"),
        ("派生表 5万", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` LIMIT 25000) t;"),
    ):
        nn = 10000 if "5万" not in label else 50000
        if "派生表" in label:
            pref.append(
                pack(
                    f"测试前缀索引下从 C {label}行的执行情况",
                    "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 0) t;",
                    idx_prefix,
                    50000,
                    bid,
                )
            )
        else:
            pref.append(
                pack(
                    f"测试前缀索引下从 C 插入{nn//10000 if nn>=10000 else 1}万行{label}的执行情况",
                    tmr,
                    idx_prefix,
                    nn,
                    bid,
                )
            )
        bid += 400_000
    pref.append(
        pack(
            "测试前缀索引下从 C 插入5万行 ORDER BY varchar_col DESC 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col` DESC;",
            idx_prefix,
            50000,
            bid,
        )
    )
    bid += 400_000
    pref.append(
        pack(
            "测试前缀索引下从 C 插入10万行 WHERE varchar_col LIKE c_% 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `varchar_col` LIKE 'c_%';",
            idx_prefix,
            100000,
            bid,
        )
    )
    bid += 400_000
    pref.append(
        pack(
            "测试前缀索引下从 C 插入1万行显式列 ORDER BY id_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `id_col`;",
            idx_prefix,
            10000,
            bid,
        )
    )
    bid += 400_000
    pref.append(
        pack(
            "测试前缀索引下从 C 插入5万行 WHERE mediumint_col IS NOT NULL 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `mediumint_col` IS NOT NULL;",
            idx_prefix,
            50000,
            bid,
        )
    )
    bid += 400_000
    pref.append(
        pack(
            "测试前缀索引下从 C 插入10万行 ORDER BY float_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `float_col`;",
            idx_prefix,
            100000,
            bid,
        )
    )
    bid += 400_000
    pref.append(
        pack(
            "测试前缀索引下从 C 插入1万行 WHERE tinyint_col=0 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `tinyint_col` = 0;",
            idx_prefix,
            10000,
            bid,
        )
    )
    bid += 400_000
    assert len(pref) == 20
    write_many("insert_prefix_index", pref)

    # insert_expression_index
    expr: list[tuple] = []
    bid = 15_000_000
    for n, lab in sizes:
        expr.append(
            pack(
                f"测试表达式索引 ABS(bigint_col) 下从 C 插入{lab}行 INSERT SELECT * 的执行情况",
                _TIMER_INSERT_STAR,
                idx_expr,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        expr.append(
            pack(
                f"测试表达式索引下从 C 插入{lab}行 ORDER BY bigint_col 的执行情况",
                "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `bigint_col`;",
                idx_expr,
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        expr.append(
            pack(
                f"测试表达式索引下从 C 插入{lab}行显式列 INSERT 的执行情况",
                _TIMER_INSERT_EXPLICIT,
                idx_expr,
                n,
                bid,
            )
        )
        bid += 400_000
    for label, tmr in (
        ("WHERE bigint_col IS NOT NULL", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `bigint_col` IS NOT NULL;"),
        ("触发 ABS 边界 bigint 模1000", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `bigint_col` % 1000 = 0;"),
        ("ORDER BY int_col", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `int_col`;"),
        ("非索引列 smallint 过滤", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `smallint_col` IS NOT NULL;"),
        ("派生表插入", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 3 = 0) t;"),
    ):
        expr.append(
            pack(
                f"测试表达式索引下从 C 插入1万行{label}的执行情况",
                tmr,
                idx_expr,
                10000,
                bid,
            )
        )
        bid += 400_000
    expr.append(
        pack(
            "测试表达式索引下从 C 插入5万行 WHERE id_col 奇数 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 1;",
            idx_expr,
            50000,
            bid,
        )
    )
    bid += 400_000
    expr.append(
        pack(
            "测试表达式索引下从 C 插入10万行 ORDER BY bigint_col DESC 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `bigint_col` DESC;",
            idx_expr,
            100000,
            bid,
        )
    )
    bid += 400_000
    expr.append(
        pack(
            "测试表达式索引下从 C 插入1万行显式列 ORDER BY bigint_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `bigint_col`;",
            idx_expr,
            10000,
            bid,
        )
    )
    bid += 400_000
    expr.append(
        pack(
            "测试表达式索引下从 C 插入5万行 WHERE bigint_col BETWEEN -1000000 AND 1000000 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `bigint_col` BETWEEN -1000000 AND 1000000;",
            idx_expr,
            50000,
            bid,
        )
    )
    bid += 400_000
    expr.append(
        pack(
            "测试表达式索引下从 C 插入10万行 WHERE bool_col IS NOT NULL 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `bool_col` IS NOT NULL;",
            idx_expr,
            100000,
            bid,
        )
    )
    bid += 400_000
    expr.append(
        pack(
            "测试表达式索引下从 C 插入1万行 ORDER BY ABS(bigint_col) 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY ABS(`bigint_col`);",
            idx_expr,
            10000,
            bid,
        )
    )
    assert len(expr) == 20
    write_many("insert_expression_index", expr)

    # insert_unique_index
    uq: list[tuple] = []
    bid = 16_000_000
    for n, lab in sizes:
        uq.append(
            pack(
                f"测试唯一索引 varchar_col 下从 C 插入{lab}行 INSERT SELECT * 的执行情况",
                _TIMER_INSERT_STAR,
                idx_unique,
                n,
                bid,
                pre_index=pre_uq,
                varchar_sel=vc_unique,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        uq.append(
            pack(
                f"测试唯一索引下从 C 插入{lab}行 ORDER BY varchar_col 的执行情况",
                "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col`;",
                idx_unique,
                n,
                bid,
                pre_index=pre_uq,
                varchar_sel=vc_unique,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        uq.append(
            pack(
                f"测试唯一索引下从 C 插入{lab}行显式列 INSERT 的执行情况",
                _TIMER_INSERT_EXPLICIT,
                idx_unique,
                n,
                bid,
                pre_index=pre_uq,
                varchar_sel=vc_unique,
            )
        )
        bid += 400_000
    for label, tmr in (
        ("WHERE id_col 模2", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 0;"),
        ("ORDER BY id_col", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `id_col`;"),
        ("非唯一列 int_col 过滤", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `int_col` BETWEEN -100000 AND 100000;"),
        ("派生表 1万", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` LIMIT 8000) t;"),
    ):
        uq.append(
            pack(
                f"测试唯一索引下从 C 插入1万行{label}的执行情况",
                tmr,
                idx_unique,
                10000,
                bid,
                pre_index=pre_uq,
                varchar_sel=vc_unique,
            )
        )
        bid += 400_000
    uq.append(
        pack(
            "测试唯一索引下从 C 插入5万行 WHERE varchar_col LIKE c_% 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `varchar_col` LIKE 'c_%';",
            idx_unique,
            50000,
            bid,
            pre_index=pre_uq,
            varchar_sel=vc_unique,
        )
    )
    bid += 400_000
    uq.append(
        pack(
            "测试唯一索引下从 C 插入10万行 ORDER BY unsigned_int_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `unsigned_int_col`;",
            idx_unique,
            100000,
            bid,
            pre_index=pre_uq,
            varchar_sel=vc_unique,
        )
    )
    uq.append(
        pack(
            "测试唯一索引下可能重复 varchar 导致插入失败边界",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` UNION ALL SELECT * FROM `{{TEST_TABLE_NAME}}_src` LIMIT 1;",
            idx_unique,
            10000,
            bid,
            pre_index=pre_uq,
            varchar_sel="'dup_vc'",
        )
    )
    bid += 400_000
    uq.append(
        pack(
            "测试唯一索引下从 C 插入5万行 ORDER BY int_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `int_col`;",
            idx_unique,
            50000,
            bid,
            pre_index=pre_uq,
            varchar_sel=vc_unique,
        )
    )
    bid += 400_000
    uq.append(
        pack(
            "测试唯一索引下从 C 插入10万行 WHERE id_col 模5 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 5 = 0;",
            idx_unique,
            100000,
            bid,
            pre_index=pre_uq,
            varchar_sel=vc_unique,
        )
    )
    bid += 400_000
    uq.append(
        pack(
            "测试唯一索引下从 C 插入1万行显式列 WHERE smallint_col IS NOT NULL 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src` WHERE `smallint_col` IS NOT NULL;",
            idx_unique,
            10000,
            bid,
            pre_index=pre_uq,
            varchar_sel=vc_unique,
        )
    )
    bid += 400_000
    uq.append(
        pack(
            "测试唯一索引下从 C 插入5万行 ORDER BY datetime_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `datetime_col`;",
            idx_unique,
            50000,
            bid,
            pre_index=pre_uq,
            varchar_sel=vc_unique,
        )
    )
    bid += 400_000
    assert len(uq) == 20
    write_many("insert_unique_index", uq)

    # insert_primary_key — no secondary index
    pk: list[tuple] = []
    bid = 17_000_000
    for n, lab in sizes:
        pk.append(
            pack(
                f"测试仅主键下从 C 插入{lab}行 INSERT SELECT * 的执行情况",
                _TIMER_INSERT_STAR,
                (),
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        pk.append(
            pack(
                f"测试仅主键下从 C 插入{lab}行 ORDER BY id_col 的执行情况",
                "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `id_col`;",
                (),
                n,
                bid,
            )
        )
        bid += 400_000
    for n, lab in sizes:
        pk.append(
            pack(
                f"测试仅主键下从 C 插入{lab}行显式列 INSERT 的执行情况",
                _TIMER_INSERT_EXPLICIT,
                (),
                n,
                bid,
            )
        )
        bid += 400_000
    for label, tmr in (
        ("WHERE 模3", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 3 = 0;"),
        ("ORDER BY bigint_col", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `bigint_col`;"),
        ("非主键列过滤 enum", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `enum_col` = 'aaa';"),
        ("派生表半量", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM (SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 2 = 0) t;"),
        ("ORDER BY datetime_col", "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `datetime_col`;"),
    ):
        pk.append(
            pack(
                f"测试仅主键下从 C 插入1万行{label}的执行情况",
                tmr,
                (),
                10000,
                bid,
            )
        )
        bid += 400_000
    pk.append(
        pack(
            "测试仅主键下从 C 插入5万行 WHERE int_col IS NOT NULL 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `int_col` IS NOT NULL;",
            (),
            50000,
            bid,
        )
    )
    bid += 400_000
    pk.append(
        pack(
            "测试仅主键下从 C 插入10万行 ORDER BY year_col,id_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `year_col`, `id_col`;",
            (),
            100000,
            bid,
        )
    )
    bid += 400_000
    pk.append(
        pack(
            "测试仅主键下从 C 插入5万行 ORDER BY varchar_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `varchar_col`;",
            (),
            50000,
            bid,
        )
    )
    bid += 400_000
    pk.append(
        pack(
            "测试仅主键下从 C 插入10万行 WHERE tinyint_col IS NOT NULL 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` WHERE `tinyint_col` IS NOT NULL;",
            (),
            100000,
            bid,
        )
    )
    bid += 400_000
    pk.append(
        pack(
            "测试仅主键下从 C 插入1万行 ORDER BY time_col 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `time_col`;",
            (),
            10000,
            bid,
        )
    )
    bid += 400_000
    pk.append(
        pack(
            "测试仅主键下从 C 插入5万行显式列 WHERE id_col 模7 的执行情况",
            "INSERT INTO `{{TEST_TABLE_NAME}}` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`) SELECT `id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col` FROM `{{TEST_TABLE_NAME}}_src` WHERE `id_col` % 7 = 0;",
            (),
            50000,
            bid,
        )
    )
    bid += 400_000
    assert len(pk) == 20
    write_many("insert_primary_key", pk)


def write_dml_update_cases() -> None:
    """Generate UPDATE benchmark cases for 7 index types, 20 cases each."""
    idx_single = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_single_int` (`int_col`);",)
    idx_desc = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_desc_vc` (`varchar_col` DESC);",)
    idx_comp = (
        "ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));",
    )
    idx_prefix = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_prefix` (`varchar_col`(32));",)
    idx_expr = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_expr` ((ABS(`bigint_col`)));",)
    pre_uq = ("UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col`;",)
    idx_unique = ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_upd_uq_uint` (`unsigned_int_col`);",)

    def pack_upd(desc: str, timer: str, idx: tuple[str, ...], pre_idx: tuple[str, ...] = ()) -> tuple:
        return item(desc, timer, (), pre_idx + idx)

    # ── update_single_index ── index on int_col ──────────────────────────
    singl = [
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 非索引列 WHERE int_col 精确匹配的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('upd_', COALESCE(`varchar_col`, '')) WHERE `int_col` = 1;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 非索引列 WHERE int_col BETWEEN 范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('rng_', COALESCE(`varchar_col`, '')) WHERE `int_col` BETWEEN -10000 AND 10000;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 非索引列 WHERE int_col IS NOT NULL 全量扫描的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('all_', COALESCE(`varchar_col`, '')) WHERE `int_col` IS NOT NULL;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 非索引列 WHERE int_col < 0 范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'neg1' WHERE `int_col` < 0;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 非索引列 WHERE int_col > 10000 高值范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'big1' WHERE `int_col` > 10000;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 索引列本身 +1 WHERE id_col 偶数的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = `int_col` + 1 WHERE `id_col` % 2 = 0;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 索引列取反 WHERE int_col > 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = -`int_col` WHERE `int_col` > 0;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 索引列设为 NULL WHERE int_col = 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = NULL WHERE `int_col` = 0;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下全表 UPDATE 无 WHERE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = 'updated_row';",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE WHERE id_col IN 少量主键的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `id_col` IN (1, 2, 3, 4, 5);",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下多列同时 UPDATE WHERE int_col > 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = `int_col` + 10, `varchar_col` = CONCAT('m_', COALESCE(`varchar_col`, '')) WHERE `int_col` > 0;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 CASE 表达式 UPDATE varchar_col WHERE int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CASE WHEN `int_col` > 0 THEN 'pos' WHEN `int_col` < 0 THEN 'neg' ELSE 'zero' END WHERE `int_col` IS NOT NULL;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE ORDER BY int_col LIMIT 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1 ORDER BY `int_col` LIMIT 1000;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE WHERE int_col > 0 LIMIT 500 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 0 WHERE `int_col` > 0 LIMIT 500;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE ORDER BY int_col DESC LIMIT 100 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 ORDER BY `int_col` DESC LIMIT 100;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE bigint_col WHERE int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` + 1000 WHERE `int_col` IS NOT NULL;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE char_col WHERE int_col 模3 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'mod3' WHERE `int_col` % 3 = 0;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE varchar_col UPPER WHERE int_col 范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = UPPER(COALESCE(`varchar_col`, '')) WHERE `int_col` BETWEEN 0 AND 10000;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下将负 int_col 取绝对值 UPDATE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = ABS(`int_col`) WHERE `int_col` < 0;",
            idx_single,
        ),
        pack_upd(
            "测试单列索引 int_col 下 UPDATE 多非索引列 WHERE int_col > 0 AND varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1, `bool_col` = 1 WHERE `int_col` > 0 AND `varchar_col` IS NOT NULL;",
            idx_single,
        ),
    ]
    assert len(singl) == 20
    write_many("update_single_index", singl)

    # ── update_desc_index ── index on varchar_col DESC ───────────────────
    desc_upd = [
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 非索引列 WHERE varchar_col 精确匹配的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `varchar_col` = 'c_0000000001';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 非索引列 WHERE varchar_col LIKE 前缀的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 1 WHERE `varchar_col` LIKE 'c_%';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 非索引列 WHERE varchar_col IS NOT NULL 全量的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 2 WHERE `varchar_col` IS NOT NULL;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 非索引列 WHERE varchar_col BETWEEN 范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = -1 WHERE `varchar_col` BETWEEN 'c_0000000000' AND 'c_0000005000';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 非索引列 WHERE varchar_col > 高值的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 99999 WHERE `varchar_col` > 'c_0000009000';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 索引列本身 CONCAT WHERE id_col 偶数的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('upd_', COALESCE(`varchar_col`, '')) WHERE `id_col` % 2 = 0;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 索引列 UPPER 全量的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = UPPER(COALESCE(`varchar_col`, '')) WHERE `varchar_col` IS NOT NULL;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 索引列 LOWER 全表无 WHERE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = LOWER(COALESCE(`varchar_col`, ''));",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 索引列设为 NULL WHERE LIKE 模糊的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = NULL WHERE `varchar_col` LIKE '%0000001%';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE ORDER BY varchar_col DESC LIMIT 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 ORDER BY `varchar_col` DESC LIMIT 1000;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE WHERE varchar_col IS NOT NULL LIMIT 500 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 WHERE `varchar_col` IS NOT NULL LIMIT 500;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE int_col WHERE varchar_col BETWEEN 范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 42 WHERE `varchar_col` BETWEEN 'a' AND 'm';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE bigint_col WHERE varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` * 2 WHERE `varchar_col` IS NOT NULL;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 索引列为唯一值 WHERE id_col 模3 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('p_', LPAD(`id_col`, 10, '0')) WHERE `id_col` % 3 = 0;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下同时 UPDATE 索引列与 int_col 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0, `varchar_col` = CONCAT('mi_', COALESCE(`varchar_col`, '')) WHERE `varchar_col` IS NOT NULL;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE bool_col WHERE varchar_col LIKE 含数字的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `varchar_col` LIKE '%0%';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE datetime_col WHERE varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2024-01-01 00:00:00' WHERE `varchar_col` IS NOT NULL AND `int_col` IS NOT NULL;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 索引列 REPLACE 替换字符 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = REPLACE(COALESCE(`varchar_col`, ''), '_', '-') WHERE `varchar_col` LIKE '%\\_%';",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE ORDER BY varchar_col ASC LIMIT 100 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'asc1' ORDER BY `varchar_col` ASC LIMIT 100;",
            idx_desc,
        ),
        pack_upd(
            "测试逆序索引 varchar_col DESC 下 UPDATE 多列非索引列 WHERE varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'abcd', `tinyint_col` = 5 WHERE `varchar_col` IS NOT NULL;",
            idx_desc,
        ),
    ]
    assert len(desc_upd) == 20
    write_many("update_desc_index", desc_upd)

    # ── update_composite_index ── index on (year_col, int_col, varchar_col(16)) ──
    comp_upd = [
        pack_upd(
            "测试组合索引下 UPDATE WHERE year_col 精确匹配首列的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'y24' WHERE `year_col` = 2024;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE WHERE year_col + int_col 两列前缀匹配的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'y2i0' WHERE `year_col` = 2024 AND `int_col` = 0;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE WHERE 三列全匹配含 varchar LIKE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 3 WHERE `year_col` = 2024 AND `int_col` = 0 AND `varchar_col` LIKE 'c_%';",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE WHERE year_col BETWEEN 范围首列的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` + 1 WHERE `year_col` BETWEEN 2020 AND 2024;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE WHERE year_col IS NOT NULL AND int_col > 0 复合条件的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `year_col` IS NOT NULL AND `int_col` > 0;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE 首列 year_col 本身 WHERE id_col 偶数的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2025 WHERE `id_col` % 2 = 0;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE 第二列 int_col WHERE year_col 精确匹配的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = `int_col` + 100 WHERE `year_col` = 2024;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE 第三列 varchar_col WHERE 前两列匹配的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('c_', COALESCE(`varchar_col`, '')) WHERE `year_col` = 2024 AND `int_col` > 0;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下全表 UPDATE 无 WHERE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = 'reset_all';",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下同时 UPDATE 多个索引列 WHERE id_col IN 少量主键的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2025, `int_col` = 0 WHERE `id_col` IN (1, 2, 3, 4, 5);",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE 非索引列 bigint_col WHERE year_col = 2024 AND int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` + 1 WHERE `year_col` = 2024 AND `int_col` IS NOT NULL;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE ORDER BY year_col, int_col LIMIT 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 7 ORDER BY `year_col`, `int_col` LIMIT 1000;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE WHERE year_col = 2024 LIMIT 500 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 8 WHERE `year_col` = 2024 LIMIT 500;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE enum_col WHERE year_col IS NOT NULL AND int_col > 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'aaa' WHERE `year_col` IS NOT NULL AND `int_col` > 0;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE 首列 year_col 为派生表达式 WHERE year_col 范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = YEAR(`date_col`) WHERE `year_col` BETWEEN 2020 AND 2030 AND `date_col` IS NOT NULL;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 CASE 表达式 UPDATE int_col WHERE year_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = CASE WHEN `year_col` < 2020 THEN 0 WHEN `year_col` = 2024 THEN 100 ELSE -1 END WHERE `year_col` IS NOT NULL;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE varchar_col 为年份+整数拼接 WHERE year_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(CAST(`year_col` AS CHAR), '_', CAST(`int_col` AS CHAR)) WHERE `year_col` IS NOT NULL;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE ORDER BY year_col DESC, int_col DESC LIMIT 200 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'dsc2' ORDER BY `year_col` DESC, `int_col` DESC LIMIT 200;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下将 year_col, int_col 同时设为 NULL WHERE id_col 模7 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = NULL, `int_col` = NULL WHERE `id_col` % 7 = 0;",
            idx_comp,
        ),
        pack_upd(
            "测试组合索引下 UPDATE tinyint_col WHERE year_col = 2024 AND varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 0 WHERE `year_col` = 2024 AND `varchar_col` IS NOT NULL;",
            idx_comp,
        ),
    ]
    assert len(comp_upd) == 20
    write_many("update_composite_index", comp_upd)

    # ── update_prefix_index ── index on varchar_col(32) ──────────────────
    pref_upd = [
        pack_upd(
            "测试前缀索引 varchar_col(32) 下 UPDATE 非索引列 WHERE varchar_col 精确匹配的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `varchar_col` = 'c_0000000001';",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 非索引列 WHERE varchar_col LIKE 前缀扫描的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 1 WHERE `varchar_col` LIKE 'c_%';",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 非索引列 WHERE varchar_col IS NOT NULL 全量的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 2 WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 非索引列 WHERE varchar_col BETWEEN 范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = -1 WHERE `varchar_col` BETWEEN 'c_0000000000' AND 'c_0000005000';",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列本身 CONCAT WHERE id_col 偶数触发前缀变更的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('prf_', COALESCE(`varchar_col`, '')) WHERE `id_col` % 2 = 0;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列 LEFT 截短改变前缀的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = LEFT(COALESCE(`varchar_col`, ''), 16) WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列 UPPER 全量触发前缀索引重建的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = UPPER(COALESCE(`varchar_col`, '')) WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列设为 NULL WHERE LIKE 模糊的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = NULL WHERE `varchar_col` LIKE '%0000001%';",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE int_col 为 CHAR_LENGTH(varchar_col) WHERE varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = CHAR_LENGTH(COALESCE(`varchar_col`, '')) WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE char_col 为 varchar_col 左4字符 WHERE varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = LEFT(COALESCE(`varchar_col`, '    '), 4) WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE ORDER BY varchar_col LIMIT 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 ORDER BY `varchar_col` LIMIT 1000;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE WHERE varchar_col > 中值 LIMIT 500 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 WHERE `varchar_col` > 'c_0000005000' LIMIT 500;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列为唯一拼接值 WHERE id_col 模5 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('new_', LPAD(`id_col`, 10, '0')) WHERE `id_col` % 5 = 0;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE enum_col WHERE varchar_col LIKE 前缀的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'bbb' WHERE `varchar_col` LIKE 'c_%';",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列 LPAD 拉长字符串影响超出前缀部分的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = LPAD(COALESCE(`varchar_col`, ''), 50, '_') WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列 SUBSTR 缩短字符串改变前缀的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = SUBSTR(COALESCE(`varchar_col`, ''), 1, 10) WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE bool_col WHERE varchar_col BETWEEN 高值范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `varchar_col` BETWEEN 'c_0000005000' AND 'c_0000009000';",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE ORDER BY varchar_col DESC LIMIT 100 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'dsc1' ORDER BY `varchar_col` DESC LIMIT 100;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE tinytext_col 为 varchar_col WHERE varchar_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinytext_col` = `varchar_col` WHERE `varchar_col` IS NOT NULL;",
            idx_prefix,
        ),
        pack_upd(
            "测试前缀索引下 UPDATE 索引列 RPAD 填充 WHERE id_col 模3 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = RPAD(COALESCE(`varchar_col`, '_'), 64, 'z') WHERE `id_col` % 3 = 0;",
            idx_prefix,
        ),
    ]
    assert len(pref_upd) == 20
    write_many("update_prefix_index", pref_upd)

    # ── update_expression_index ── index on (ABS(bigint_col)) ────────────
    expr_upd = [
        pack_upd(
            "测试表达式索引 ABS(bigint_col) 下 UPDATE 非索引列 WHERE bigint_col IS NOT NULL 全量的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = SIGN(`bigint_col`) WHERE `bigint_col` IS NOT NULL;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 非索引列 WHERE bigint_col < 0 命中负值的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'neg2' WHERE `bigint_col` < 0;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 非索引列 WHERE ABS(bigint_col) = 0 精确命中表达式值的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 WHERE ABS(`bigint_col`) = 0;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 源列 bigint_col +1 WHERE id_col 偶数触发表达式索引更新的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` + 1 WHERE `id_col` % 2 = 0;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 源列 bigint_col 取反 WHERE bigint_col > 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = -`bigint_col` WHERE `bigint_col` > 0;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 源列 bigint_col 取绝对值 WHERE bigint_col < 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = ABS(`bigint_col`) WHERE `bigint_col` < 0;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下全表 UPDATE 源列 bigint_col -1 无 WHERE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` - 1;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 源列 bigint_col 设为 NULL WHERE bigint_col < -1000000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = NULL WHERE `bigint_col` < -1000000;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE ORDER BY ABS(bigint_col) LIMIT 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1 ORDER BY ABS(`bigint_col`) LIMIT 1000;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 源列 bigint_col *2 WHERE ABS(bigint_col) < 100 命中表达式索引范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` * 2 WHERE ABS(`bigint_col`) < 100;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 源列 bigint_col = id_col*10000 WHERE id_col 模5 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CAST(`id_col` AS SIGNED) * 10000 WHERE `id_col` % 5 = 0;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE smallint_col = bigint_col 取模 WHERE bigint_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `smallint_col` = CAST(`bigint_col` % 32767 AS SIGNED) WHERE `bigint_col` IS NOT NULL;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE WHERE ABS(bigint_col) BETWEEN 范围 LIMIT 500 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE ABS(`bigint_col`) BETWEEN 0 AND 1000 LIMIT 500;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE bool_col IF(bigint_col>0) WHERE bigint_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = IF(`bigint_col` > 0, 1, 0) WHERE `bigint_col` IS NOT NULL;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 CASE 将 bigint_col 全部变正数的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CASE WHEN `bigint_col` IS NULL THEN NULL WHEN `bigint_col` >= 0 THEN `bigint_col` ELSE -`bigint_col` END;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE 源列 bigint_col = 9999999 WHERE id_col IN 少量主键的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = 9999999 WHERE `id_col` IN (1, 100, 1000);",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE ORDER BY bigint_col LIMIT 200 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 9 ORDER BY `bigint_col` LIMIT 200;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE varchar_col = CAST(bigint_col AS CHAR) WHERE bigint_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CAST(`bigint_col` AS CHAR) WHERE `bigint_col` IS NOT NULL;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE bigint_col = int_col*1000 并 mediumint_col 同时更新的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CAST(`int_col` AS SIGNED) * 1000, `mediumint_col` = ABS(`int_col`) % 8388607 WHERE `int_col` IS NOT NULL;",
            idx_expr,
        ),
        pack_upd(
            "测试表达式索引下 UPDATE bigint_col = 0 将表达式索引全部置零的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = 0 WHERE `bigint_col` IS NOT NULL;",
            idx_expr,
        ),
    ]
    assert len(expr_upd) == 20
    write_many("update_expression_index", expr_upd)

    # ── update_unique_index ── unique index on unsigned_int_col ──────────
    uq_upd = [
        pack_upd(
            "测试唯一索引 unsigned_int_col 下 UPDATE 非索引列 WHERE unsigned_int_col 精确点查的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = 'found' WHERE `unsigned_int_col` = 1000;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE 非索引列 WHERE unsigned_int_col BETWEEN 小范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `unsigned_int_col` BETWEEN 1 AND 100;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE 非索引列 WHERE unsigned_int_col IS NOT NULL 全量的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `unsigned_int_col` IS NOT NULL;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE 非索引列 WHERE unsigned_int_col > 高值的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'big2' WHERE `unsigned_int_col` > 5000;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE 非索引列 WHERE unsigned_int_col IN 列表的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 5 WHERE `unsigned_int_col` IN (1, 10, 100, 1000, 10000);",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下全表 UPDATE 非唯一列 varchar_col 无 WHERE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('u_', LPAD(`id_col`, 10, '0'));",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE ORDER BY unsigned_int_col LIMIT 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 ORDER BY `unsigned_int_col` LIMIT 1000;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE WHERE unsigned_int_col > 5000 LIMIT 500 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `unsigned_int_col` > 5000 LIMIT 500;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE int_col = unsigned_int_col 取模 WHERE unsigned_int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = CAST(`unsigned_int_col` % 1000 AS SIGNED) WHERE `unsigned_int_col` IS NOT NULL;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE bigint_col WHERE unsigned_int_col < 5000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CAST(`unsigned_int_col` AS SIGNED) * 100 WHERE `unsigned_int_col` < 5000;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 CASE 表达式 UPDATE enum_col WHERE unsigned_int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = CASE WHEN `unsigned_int_col` % 3 = 0 THEN 'aaa' WHEN `unsigned_int_col` % 3 = 1 THEN 'bbb' ELSE 'ccc' END WHERE `unsigned_int_col` IS NOT NULL;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE year_col 派生自 unsigned_int_col 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2000 + CAST(`unsigned_int_col` % 24 AS UNSIGNED) WHERE `unsigned_int_col` IS NOT NULL;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE ORDER BY unsigned_int_col DESC LIMIT 200 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'dsc3' ORDER BY `unsigned_int_col` DESC LIMIT 200;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE varchar_col WHERE unsigned_int_col BETWEEN 中间范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('uid_', `unsigned_int_col`) WHERE `unsigned_int_col` BETWEEN 1000 AND 5000;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE tinyint_col WHERE unsigned_int_col < 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = CAST(`unsigned_int_col` % 127 AS UNSIGNED) WHERE `unsigned_int_col` < 1000;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE char_col 为 LPAD(unsigned_int_col) WHERE unsigned_int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = LPAD(CAST(`unsigned_int_col` % 9999 AS CHAR), 4, '0') WHERE `unsigned_int_col` IS NOT NULL;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE bool_col 按奇偶 WHERE unsigned_int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = (`unsigned_int_col` % 2 = 0) WHERE `unsigned_int_col` IS NOT NULL;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE decimal_col WHERE unsigned_int_col BETWEEN 小额区间的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `decimal_col` = CAST(`unsigned_int_col` AS DECIMAL(25,5)) * 0.01 WHERE `unsigned_int_col` BETWEEN 100 AND 10000;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE datetime_col 加秒偏移 WHERE unsigned_int_col < 100 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = DATE_ADD(COALESCE(`datetime_col`, NOW()), INTERVAL CAST(`unsigned_int_col` % 3600 AS UNSIGNED) SECOND) WHERE `unsigned_int_col` < 100;",
            idx_unique,
            pre_uq,
        ),
        pack_upd(
            "测试唯一索引下 UPDATE float_col WHERE unsigned_int_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `float_col` = CAST(`unsigned_int_col` AS FLOAT) / 1000.0 WHERE `unsigned_int_col` IS NOT NULL;",
            idx_unique,
            pre_uq,
        ),
    ]
    assert len(uq_upd) == 20
    write_many("update_unique_index", uq_upd)

    # ── update_primary_key ── no secondary index ──────────────────────────
    pk_upd = [
        pack_upd(
            "测试仅主键下 UPDATE 单行 WHERE id_col 精确点查的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = 'pk_hit' WHERE `id_col` = 1;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col BETWEEN 小范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `id_col` BETWEEN 1 AND 100;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col > 5000 大范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'big3' WHERE `id_col` > 5000 AND `id_col` <= 10000;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col IN 离散少量主键的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1, `tinyint_col` = 10 WHERE `id_col` IN (1, 10, 100, 1000, 10000);",
            (),
        ),
        pack_upd(
            "测试仅主键下全表 UPDATE 无 WHERE 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = 'full_pk';",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col % 2 = 0 半表的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('pk_', LPAD(`id_col`, 10, '0')) WHERE `id_col` % 2 = 0;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE ORDER BY id_col LIMIT 1000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1 ORDER BY `id_col` LIMIT 1000;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col < 1000 LIMIT 200 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 0 WHERE `id_col` < 1000 LIMIT 200;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col IS NOT NULL 全表含 NULL 安全条件的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'bbb' WHERE `id_col` IS NOT NULL;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE ORDER BY id_col DESC LIMIT 500 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 ORDER BY `id_col` DESC LIMIT 500;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col % 5 = 0 五分之一行的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CAST(`id_col` AS SIGNED) * 1000 WHERE `id_col` % 5 = 0;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE WHERE id_col BETWEEN 大范围的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2024 WHERE `id_col` BETWEEN 1 AND 10000;",
            (),
        ),
        pack_upd(
            "测试仅主键下多列同时 UPDATE WHERE id_col % 3 = 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = -`id_col`, `varchar_col` = CONCAT('mult_', LPAD(`id_col`, 6, '0')) WHERE `id_col` % 3 = 0;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE ORDER BY id_col LIMIT 2000 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'lim2' ORDER BY `id_col` LIMIT 2000;",
            (),
        ),
        pack_upd(
            "测试仅主键下 CASE 表达式 UPDATE int_col WHERE id_col IS NOT NULL 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = CASE WHEN `id_col` % 3 = 0 THEN 0 WHEN `id_col` % 3 = 1 THEN 1 ELSE -1 END WHERE `id_col` IS NOT NULL;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE 两非索引列 WHERE id_col % 7 = 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1, `tinyint_col` = 100 WHERE `id_col` % 7 = 0;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE 非索引列设为 NULL WHERE id_col IN 少量主键的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = NULL WHERE `id_col` IN (1, 2, 3, 4, 5);",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE decimal_col WHERE id_col % 4 = 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `decimal_col` = CAST(`id_col` AS DECIMAL(25,5)) * 1.5 WHERE `id_col` % 4 = 0;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE datetime_col WHERE id_col < 100 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2024-06-15 12:00:00' WHERE `id_col` < 100;",
            (),
        ),
        pack_upd(
            "测试仅主键下 UPDATE set_col + enum_col WHERE id_col % 11 = 0 的执行情况",
            "UPDATE `{{TEST_TABLE_NAME}}` SET `set_col` = '111,222', `enum_col` = 'ccc' WHERE `id_col` % 11 = 0;",
            (),
        ),
    ]
    assert len(pk_upd) == 20
    write_many("update_primary_key", pk_upd)


def main() -> None:
    rn_extra = (
        "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r`;",
        "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_rn`;",
    )

    # 1) Renaming a column
    # Official InnoDB online DDL docs list CHANGE with the same type for column rename.
    renames = [
        ("测试使用 CHANGE 将 int_col 重命名为 int_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `int_col` `int_col_r1` mediumint;"),
        ("测试使用 CHANGE 将 bigint_col 重命名为 bigint_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bigint_col` `bigint_col_r1` bigint;"),
        ("测试使用 CHANGE 将 year_col 重命名为 year_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `year_col` `year_col_r1` year;"),
        ("测试使用 CHANGE 将 char_col 重命名为 char_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `char_col` `char_col_r1` char(4);"),
        ("测试使用 CHANGE 将 tinyint_col 重命名为 tinyint_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `tinyint_col` `tinyint_col_r1` tinyint unsigned;"),
        ("测试使用 CHANGE 将 bool_col 重命名为 bool_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bool_col` `bool_col_r1` tinyint(1);"),
        ("测试使用 CHANGE 将 smallint_col 重命名为 smallint_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `smallint_col` `smallint_col_r1` smallint;"),
        ("测试使用 CHANGE 将 mediumint_col 重命名为 mediumint_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `mediumint_col` `mediumint_col_r1` mediumint unsigned;"),
        ("测试使用 CHANGE 将 decimal_col 重命名为 decimal_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `decimal_col` `decimal_col_r1` decimal(25,5) unsigned;"),
        ("测试使用 CHANGE 将 float_col 重命名为 float_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `float_col` `float_col_r1` float unsigned;"),
        ("测试使用 CHANGE 将 date_col 重命名为 date_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `date_col` `date_col_r1` date DEFAULT NULL;"),
        ("测试使用 CHANGE 将 datetime_col 重命名为 datetime_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `datetime_col` `datetime_col_r1` datetime(6);"),
        ("测试使用 CHANGE 将 timestamp_col 重命名为 timestamp_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `timestamp_col` `timestamp_col_r1` timestamp NULL DEFAULT NULL;"),
        ("测试使用 CHANGE 将 time_col 重命名为 time_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `time_col` `time_col_r1` time;"),
        ("测试使用 CHANGE 将 varchar_col 重命名为 varchar_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varchar_col` `varchar_col_r1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"),
        ("测试使用 CHANGE 将 binary_col 重命名为 binary_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `binary_col` `binary_col_r1` binary(1) DEFAULT NULL;"),
        ("测试使用 CHANGE 将 varbinary_col 重命名为 varbinary_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varbinary_col` `varbinary_col_r1` varbinary(255);"),
        ("测试使用 CHANGE 将 enum_col 重命名为 enum_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `enum_col` `enum_col_r1` enum('aaa','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"),
        ("测试使用 CHANGE 将 set_col 重命名为 set_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `set_col` `set_col_r1` set('111','222','333') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"),
        ("测试使用 CHANGE 将 bit_col 重命名为 bit_col_r1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bit_col` `bit_col_r1` bit(8) DEFAULT b'10011001';"),
    ]
    write_many("alter_rename_column", [(a, b, ()) for a, b in renames])

    # 2) Reordering columns
    # Official InnoDB online DDL docs say to use FIRST or AFTER in CHANGE or MODIFY operations.
    reorder = [
        ("测试使用 MODIFY 将 int_col 调整到 varchar_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `int_col` mediumint AFTER `varchar_col`;"),
        ("测试使用 MODIFY 将 bigint_col 调整到表首的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bigint_col` bigint FIRST;"),
        ("测试使用 CHANGE 将 year_col 调整到 char_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `year_col` `year_col` year AFTER `char_col`;"),
        ("测试使用 MODIFY 将 char_col 调整到 id_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `char_col` char(4) AFTER `id_col`;"),
        ("测试使用 CHANGE 将 tinyint_col 调整到 smallint_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `tinyint_col` `tinyint_col` tinyint unsigned AFTER `smallint_col`;"),
        ("测试使用 MODIFY 将 bool_col 调整到 year_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bool_col` tinyint(1) AFTER `year_col`;"),
        ("测试使用 CHANGE 将 smallint_col 调整到表首的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `smallint_col` `smallint_col` smallint FIRST;"),
        ("测试使用 MODIFY 将 mediumint_col 调整到 bool_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `mediumint_col` mediumint unsigned AFTER `bool_col`;"),
        ("测试使用 CHANGE 将 decimal_col 调整到 float_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `decimal_col` `decimal_col` decimal(25,5) unsigned AFTER `float_col`;"),
        ("测试使用 MODIFY 将 float_col 调整到 double_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `float_col` float unsigned AFTER `double_col`;"),
        ("测试使用 CHANGE 将 date_col 调整到 time_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `date_col` `date_col` date DEFAULT NULL AFTER `time_col`;"),
        ("测试使用 MODIFY 将 datetime_col 调整到 date_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `datetime_col` datetime(6) AFTER `date_col`;"),
        ("测试使用 CHANGE 将 timestamp_col 调整到 datetime_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `timestamp_col` `timestamp_col` timestamp NULL DEFAULT NULL AFTER `datetime_col`;"),
        ("测试使用 MODIFY 将 time_col 调整到表首的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `time_col` time FIRST;"),
        ("测试使用 CHANGE 将 varchar_col 调整到 set_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varchar_col` `varchar_col` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin AFTER `set_col`;"),
        ("测试使用 MODIFY 将 binary_col 调整到 enum_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `binary_col` binary(1) DEFAULT NULL AFTER `enum_col`;"),
        ("测试使用 CHANGE 将 varbinary_col 调整到 binary_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varbinary_col` `varbinary_col` varbinary(255) AFTER `binary_col`;"),
        ("测试使用 MODIFY 将 enum_col 调整到 mediumtext_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin AFTER `mediumtext_col`;"),
        ("测试使用 CHANGE 将 set_col 调整到 enum_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `set_col` `set_col` set('111','222','333') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin AFTER `enum_col`;"),
        ("测试使用 MODIFY 将 bit_col 调整到 varbinary_col 之后的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bit_col` bit(8) DEFAULT b'10011001' AFTER `varbinary_col`;"),
    ]
    write_many("alter_column_reorder", [(a, b, ()) for a, b in reorder])

    # 3) Setting a column default value
    defaults = [
        ("测试将 int_col 默认值设置为 0 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `int_col` SET DEFAULT 0;"),
        ("测试将 bigint_col 默认值设置为 -1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bigint_col` SET DEFAULT -1;"),
        ("测试将 year_col 默认值设置为 2024 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `year_col` SET DEFAULT 2024;"),
        ("测试将 char_col 默认值设置为 'ab' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `char_col` SET DEFAULT 'ab';"),
        ("测试将 tinyint_col 默认值设置为 1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `tinyint_col` SET DEFAULT 1;"),
        ("测试将 bool_col 默认值设置为 0 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bool_col` SET DEFAULT 0;"),
        ("测试将 smallint_col 默认值设置为 -12 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `smallint_col` SET DEFAULT -12;"),
        ("测试将 mediumint_col 默认值设置为 100 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `mediumint_col` SET DEFAULT 100;"),
        ("测试将 decimal_col 默认值设置为 123.45000 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `decimal_col` SET DEFAULT 123.45000;"),
        ("测试将 float_col 默认值设置为 3.5 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `float_col` SET DEFAULT 3.5;"),
        ("测试将 date_col 默认值设置为 '2001-01-01' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `date_col` SET DEFAULT '2001-01-01';"),
        ("测试将 datetime_col 默认值设置为 '2001-01-01 01:02:03.123456' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `datetime_col` SET DEFAULT '2001-01-01 01:02:03.123456';"),
        ("测试将 timestamp_col 默认值设置为 '2001-01-01 01:02:03' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `timestamp_col` SET DEFAULT '2001-01-01 01:02:03';"),
        ("测试将 time_col 默认值设置为 '12:34:56' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `time_col` SET DEFAULT '12:34:56';"),
        ("测试将 varchar_col 默认值设置为 'default_varchar' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `varchar_col` SET DEFAULT 'default_varchar';"),
        ("测试将 binary_col 默认值设置为 x'41' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `binary_col` SET DEFAULT x'41';"),
        ("测试将 varbinary_col 默认值设置为 x'4243' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `varbinary_col` SET DEFAULT x'4243';"),
        ("测试将 enum_col 默认值设置为 'bbb' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `enum_col` SET DEFAULT 'bbb';"),
        ("测试将 set_col 默认值设置为 '111,333' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `set_col` SET DEFAULT '111,333';"),
        ("测试将 bit_col 默认值设置为 b'01010101' 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bit_col` SET DEFAULT b'01010101';"),
    ]
    write_many("alter_column_default", [(a, b, ()) for a, b in defaults])

    # 4) Changing the column data type
    ctypes = [
        ("测试将 int_col 从 mediumint 改为 int 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `int_col` `int_col` int;"),
        ("测试将 bigint_col 从 bigint 改为 decimal(20,0) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bigint_col` `bigint_col` decimal(20,0);"),
        ("测试将 year_col 从 year 改为 smallint 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `year_col` `year_col` smallint;"),
        ("测试将 char_col 从 char(4) 改为 varchar(16) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `char_col` `char_col` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"),
        ("测试将 tinyint_col 从 tinyint unsigned 改为 smallint unsigned 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `tinyint_col` `tinyint_col` smallint unsigned;"),
        ("测试将 bool_col 从 tinyint(1) 改为 bit(1) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bool_col` `bool_col` bit(1) DEFAULT b'0';"),
        ("测试将 mediumint_col 从 mediumint unsigned 改为 bigint unsigned 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `mediumint_col` `mediumint_col` bigint unsigned;"),
        ("测试将 decimal_col 从 decimal(25,5) unsigned 改为 decimal(30,10) unsigned 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `decimal_col` `decimal_col` decimal(30,10) unsigned;"),
        ("测试将 float_col 从 float unsigned 改为 double unsigned 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `float_col` `float_col` double unsigned;"),
        ("测试将 double_col 从 double unsigned 改为 decimal(30,10) unsigned 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `double_col` `double_col` decimal(30,10) unsigned;"),
        ("测试将 date_col 从 date 改为 datetime 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `date_col` `date_col` datetime DEFAULT NULL;"),
        ("测试将 datetime_col 从 datetime(6) 改为 datetime(3) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `datetime_col` `datetime_col` datetime(3);"),
        ("测试将 timestamp_col 从 timestamp 改为 datetime 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `timestamp_col` `timestamp_col` datetime DEFAULT NULL;"),
        ("测试将 time_col 从 time 改为 time(3) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `time_col` `time_col` time(3);"),
        ("测试将 varchar_col 从 varchar(255) 改为 char(255) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varchar_col` `varchar_col` char(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"),
        ("测试将 binary_col 从 binary(1) 改为 varbinary(8) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `binary_col` `binary_col` varbinary(8) DEFAULT NULL;"),
        ("测试将 varbinary_col 从 varbinary(255) 改为 binary(255) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varbinary_col` `varbinary_col` binary(255);"),
        ("测试将 enum_col 从 enum 改为 varchar(16) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `enum_col` `enum_col` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"),
        ("测试将 set_col 从 set 改为 varchar(32) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `set_col` `set_col` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"),
        ("测试将 bit_col 从 bit(8) 改为 bit(16) 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bit_col` `bit_col` bit(16) DEFAULT b'1001100110011001';"),
    ]
    write_many("alter_modify_column_type", [(a, b, ()) for a, b in ctypes])

    # 5) Extending VARCHAR column size
    extend = [
        (
            f"测试将 varchar_col 扩展到 varchar({sz}) 的执行情况",
            f"ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varchar_col` `varchar_col` varchar({sz}) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;",
        )
        for sz in (256, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 512, 640, 768, 900, 1024, 1536, 2048)
    ]
    assert len(extend) == 20
    write_many("alter_extend_varchar", [(a, b, ()) for a, b in extend])

    # 6) Dropping a column default value
    drop_defaults = [
        item(
            "测试删除 int_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `int_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `int_col` SET DEFAULT 0;",),
        ),
        item(
            "测试删除 bigint_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bigint_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bigint_col` SET DEFAULT -1;",),
        ),
        item(
            "测试删除 year_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `year_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `year_col` SET DEFAULT 2024;",),
        ),
        item(
            "测试删除 char_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `char_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `char_col` SET DEFAULT 'ab';",),
        ),
        item(
            "测试删除 tinyint_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `tinyint_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `tinyint_col` SET DEFAULT 1;",),
        ),
        item(
            "测试删除 bool_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bool_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bool_col` SET DEFAULT 0;",),
        ),
        item(
            "测试删除 smallint_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `smallint_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `smallint_col` SET DEFAULT -12;",),
        ),
        item(
            "测试删除 mediumint_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `mediumint_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `mediumint_col` SET DEFAULT 100;",),
        ),
        item(
            "测试删除 decimal_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `decimal_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `decimal_col` SET DEFAULT 123.45000;",),
        ),
        item(
            "测试删除 float_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `float_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `float_col` SET DEFAULT 3.5;",),
        ),
        item(
            "测试删除 date_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `date_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `date_col` SET DEFAULT '2001-01-01';",),
        ),
        item(
            "测试删除 datetime_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `datetime_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `datetime_col` SET DEFAULT '2001-01-01 01:02:03.123456';",),
        ),
        item(
            "测试删除 timestamp_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `timestamp_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `timestamp_col` SET DEFAULT '2001-01-01 01:02:03';",),
        ),
        item(
            "测试删除 time_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `time_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `time_col` SET DEFAULT '12:34:56';",),
        ),
        item(
            "测试删除 varchar_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `varchar_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `varchar_col` SET DEFAULT 'default_varchar';",),
        ),
        item(
            "测试删除 binary_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `binary_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `binary_col` SET DEFAULT x'41';",),
        ),
        item(
            "测试删除 varbinary_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `varbinary_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `varbinary_col` SET DEFAULT x'4243';",),
        ),
        item(
            "测试删除 enum_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `enum_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `enum_col` SET DEFAULT 'bbb';",),
        ),
        item(
            "测试删除 set_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `set_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `set_col` SET DEFAULT '111,333';",),
        ),
        item(
            "测试删除 bit_col 默认值的执行情况",
            "ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bit_col` DROP DEFAULT;",
            tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ALTER COLUMN `bit_col` SET DEFAULT b'01010101';",),
        ),
    ]
    write_many("alter_column_drop_default", drop_defaults)

    # 7) Changing the auto-increment value
    autoinc = [
        (f"测试将 AUTO_INCREMENT 设置为 {v} 的执行情况", f"ALTER TABLE `{{TEST_TABLE_NAME}}` AUTO_INCREMENT = {v};")
        for v in (1, 2, 10, 50, 100, 256, 512, 1024, 2048, 4096, 5000, 8192, 10000, 12000, 15000, 20000, 30000, 50000, 65535, 100000)
    ]
    assert len(autoinc) == 20
    write_many("alter_auto_increment", [(a, b, ()) for a, b in autoinc])

    # 8) Making a column NULL
    make_nulls = [
        item("测试将 int_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `int_col` mediumint NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `int_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `int_col` mediumint NOT NULL;")),
        item("测试将 bigint_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bigint_col` bigint NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = 0 WHERE `bigint_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bigint_col` bigint NOT NULL;")),
        item("测试将 year_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `year_col` year NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2024 WHERE `year_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `year_col` year NOT NULL;")),
        item("测试将 char_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `char_col` char(4) NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'ab' WHERE `char_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `char_col` char(4) NOT NULL;")),
        item("测试将 tinyint_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `tinyint_col` tinyint unsigned NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1 WHERE `tinyint_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `tinyint_col` tinyint unsigned NOT NULL;")),
        item("测试将 bool_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bool_col` tinyint(1) NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 WHERE `bool_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bool_col` tinyint(1) NOT NULL;")),
        item("测试将 smallint_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `smallint_col` smallint NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `smallint_col` = 0 WHERE `smallint_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `smallint_col` smallint NOT NULL;")),
        item("测试将 mediumint_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `mediumint_col` mediumint unsigned NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `mediumint_col` = 1 WHERE `mediumint_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `mediumint_col` mediumint unsigned NOT NULL;")),
        item("测试将 decimal_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `decimal_col` decimal(25,5) unsigned NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `decimal_col` = 0 WHERE `decimal_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `decimal_col` decimal(25,5) unsigned NOT NULL;")),
        item("测试将 float_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `float_col` float unsigned NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `float_col` = 0 WHERE `float_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `float_col` float unsigned NOT NULL;")),
        item("测试将 double_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `double_col` double unsigned NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `double_col` = 0 WHERE `double_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `double_col` double unsigned NOT NULL;")),
        item("测试将 date_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `date_col` date NULL DEFAULT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `date_col` = '2001-01-01' WHERE `date_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `date_col` date NOT NULL;")),
        item("测试将 datetime_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `datetime_col` datetime(6) NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2001-01-01 01:02:03.123456' WHERE `datetime_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `datetime_col` datetime(6) NOT NULL;")),
        item("测试将 timestamp_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `timestamp_col` timestamp NULL DEFAULT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `timestamp_col` = '2001-01-01 01:02:03' WHERE `timestamp_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `timestamp_col` timestamp NOT NULL;")),
        item("测试将 time_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `time_col` time NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `time_col` = '12:34:56' WHERE `time_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `time_col` time NOT NULL;")),
        item("测试将 varchar_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `varchar_col` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = 'notnull' WHERE `varchar_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `varchar_col` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;")),
        item("测试将 binary_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `binary_col` binary(1) NULL DEFAULT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `binary_col` = x'41' WHERE `binary_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `binary_col` binary(1) NOT NULL;")),
        item("测试将 varbinary_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `varbinary_col` varbinary(255) NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `varbinary_col` = x'4243' WHERE `varbinary_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `varbinary_col` varbinary(255) NOT NULL;")),
        item("测试将 enum_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'aaa' WHERE `enum_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;")),
        item("测试将 set_col 修改为 NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `set_col` = '111' WHERE `set_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;")),
    ]
    write_many("alter_column_null", make_nulls)

    # 9) Making a column NOT NULL
    make_not_nulls = [
        item("测试将 int_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `int_col` mediumint NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `int_col` IS NULL;",)),
        item("测试将 bigint_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bigint_col` bigint NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = 0 WHERE `bigint_col` IS NULL;",)),
        item("测试将 year_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `year_col` year NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2024 WHERE `year_col` IS NULL;",)),
        item("测试将 char_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `char_col` char(4) NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'ab' WHERE `char_col` IS NULL;",)),
        item("测试将 tinyint_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `tinyint_col` tinyint unsigned NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1 WHERE `tinyint_col` IS NULL;",)),
        item("测试将 bool_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `bool_col` tinyint(1) NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 0 WHERE `bool_col` IS NULL;",)),
        item("测试将 smallint_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `smallint_col` smallint NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `smallint_col` = 0 WHERE `smallint_col` IS NULL;",)),
        item("测试将 mediumint_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `mediumint_col` mediumint unsigned NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `mediumint_col` = 1 WHERE `mediumint_col` IS NULL;",)),
        item("测试将 decimal_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `decimal_col` decimal(25,5) unsigned NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `decimal_col` = 0 WHERE `decimal_col` IS NULL;",)),
        item("测试将 float_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `float_col` float unsigned NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `float_col` = 0 WHERE `float_col` IS NULL;",)),
        item("测试将 double_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `double_col` double unsigned NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `double_col` = 0 WHERE `double_col` IS NULL;",)),
        item("测试将 date_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `date_col` date NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `date_col` = '2001-01-01' WHERE `date_col` IS NULL;",)),
        item("测试将 datetime_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `datetime_col` datetime(6) NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2001-01-01 01:02:03.123456' WHERE `datetime_col` IS NULL;",)),
        item("测试将 timestamp_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `timestamp_col` timestamp NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `timestamp_col` = '2001-01-01 01:02:03' WHERE `timestamp_col` IS NULL;",)),
        item("测试将 time_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `time_col` time NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `time_col` = '12:34:56' WHERE `time_col` IS NULL;",)),
        item("测试将 varchar_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `varchar_col` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = 'notnull' WHERE `varchar_col` IS NULL;",)),
        item("测试将 binary_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `binary_col` binary(1) NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `binary_col` = x'41' WHERE `binary_col` IS NULL;",)),
        item("测试将 varbinary_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `varbinary_col` varbinary(255) NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `varbinary_col` = x'4243' WHERE `varbinary_col` IS NULL;",)),
        item("测试将 enum_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'aaa' WHERE `enum_col` IS NULL;",)),
        item("测试将 set_col 修改为 NOT NULL 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `set_col` = '111' WHERE `set_col` IS NULL;",)),
    ]
    write_many("alter_column_not_null", make_not_nulls)

    # 10) Modifying the definition of an ENUM or SET column
    es = [
        ("测试向 enum_col 末尾追加 1 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 末尾追加 2 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 末尾追加 3 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 末尾追加 4 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff','ggg') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 末尾追加 5 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff','ggg','hhh') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 末尾追加 6 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff','ggg','hhh','iii') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 末尾追加 7 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff','ggg','hhh','iii','jjj') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 末尾追加 8 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff','ggg','hhh','iii','jjj','kkk') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 enum_col 中间插入新成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','ddd','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试重排 enum_col 成员顺序的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('ccc','bbb','aaa') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 1 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 2 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444','555') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 3 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444','555','666') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 4 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444','555','666','777') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 5 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444','555','666','777','888') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 6 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444','555','666','777','888','999') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 7 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444','555','666','777','888','999','000') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 末尾追加 8 个成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','222','333','444','555','666','777','888','999','000','abc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试向 set_col 中间插入新成员的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('111','444','222','333') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
        ("测试重排 set_col 成员顺序的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `set_col` set('333','222','111') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;"),
    ]
    assert len(es) == 20
    write_many("alter_enum_set_modify", es)

    # 9) ROW_FORMAT cycle
    rf = [
        ("ROW_FORMAT DYNAMIC", "ALTER TABLE `{{TEST_TABLE_NAME}}` ROW_FORMAT=DYNAMIC;"),
        ("ROW_FORMAT REDUNDANT", "ALTER TABLE `{{TEST_TABLE_NAME}}` ROW_FORMAT=REDUNDANT;"),
        ("ROW_FORMAT COMPACT", "ALTER TABLE `{{TEST_TABLE_NAME}}` ROW_FORMAT=COMPACT;"),
        ("ROW_FORMAT DYNAMIC 再设", "ALTER TABLE `{{TEST_TABLE_NAME}}` ROW_FORMAT=DYNAMIC;"),
        ("ROW_FORMAT DEFAULT", "ALTER TABLE `{{TEST_TABLE_NAME}}` ROW_FORMAT=DEFAULT;"),
    ]
    rf20 = [(f"ROW_FORMAT 轮换 {k+1}", s) for k, (_, s) in enumerate((rf * 4)[:20])]
    write_many("alter_table_row_format", [(a, b, ()) for a, b in rf20])

    # 10) Statistics
    stats = []
    for i in range(20):
        persist, recalc, pages = i % 2, (i // 2) % 2, 10 + (i * 7) % 50
        stats.append(
            (
                f"STATS 组合 persist={persist} recalc={recalc} pages={pages}",
                f"ALTER TABLE `{{TEST_TABLE_NAME}}` STATS_PERSISTENT={persist}, STATS_AUTO_RECALC={recalc}, STATS_SAMPLE_PAGES={pages};",
            )
        )
    write_many("alter_table_statistics", [(a, b, ()) for a, b in stats])

    # 11) Specifying a character set
    cs = [
        ("测试将表字符集指定为 utf8mb4 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4;"),
        ("测试将表字符集指定为 utf8mb4 且排序规则为 utf8mb4_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin;"),
        ("测试将表字符集指定为 utf8mb4 且排序规则为 utf8mb4_general_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;"),
        ("测试将表字符集指定为 utf8mb4 且排序规则为 utf8mb4_unicode_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"),
        ("测试将表字符集指定为 utf8mb4 且排序规则为 utf8mb4_0900_ai_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;"),
        ("测试将表字符集指定为 utf8mb4 且排序规则为 utf8mb4_0900_as_cs 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_as_cs;"),
        ("测试将表字符集指定为 utf8mb3 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb3;"),
        ("测试将表字符集指定为 utf8mb3 且排序规则为 utf8mb3_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb3 COLLATE = utf8mb3_bin;"),
        ("测试将表字符集指定为 utf8mb3 且排序规则为 utf8mb3_general_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci;"),
        ("测试将表字符集指定为 latin1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = latin1;"),
        ("测试将表字符集指定为 latin1 且排序规则为 latin1_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = latin1 COLLATE = latin1_bin;"),
        ("测试将表字符集指定为 latin1 且排序规则为 latin1_swedish_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = latin1 COLLATE = latin1_swedish_ci;"),
        ("测试将表字符集指定为 ascii 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = ascii;"),
        ("测试将表字符集指定为 ascii 且排序规则为 ascii_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = ascii COLLATE = ascii_bin;"),
        ("测试将表字符集指定为 ascii 且排序规则为 ascii_general_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = ascii COLLATE = ascii_general_ci;"),
        ("测试将表字符集指定为 gbk 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = gbk;"),
        ("测试将表字符集指定为 gbk 且排序规则为 gbk_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = gbk COLLATE = gbk_bin;"),
        ("测试将表字符集指定为 gbk 且排序规则为 gbk_chinese_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = gbk COLLATE = gbk_chinese_ci;"),
        ("测试将表字符集指定为 utf8mb4 且排序规则为 utf8mb4_0900_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_bin;"),
        ("测试将表字符集最终指定为 utf8mb4 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CHARACTER SET = utf8mb4;"),
    ]
    assert len(cs) == 20
    write_many("alter_table_default_charset", [(a, b, ()) for a, b in cs])

    # 12) RENAME TABLE
    rt = []
    for i in range(20):
        t2 = f"`{{{{TEST_TABLE_NAME}}}}_r{i}`"
        rt.append(
            (
                f"RENAME TABLE 到 _r{i}",
                f"RENAME TABLE `{{{{TEST_TABLE_NAME}}}}` TO `{{{{TEST_TABLE_NAME}}}}_r{i}`;",
                rn_extra,
            )
        )
    # fix f-string - I used wrong escaping. Template should be literal {{TEST_TABLE_NAME}}
    rt = []
    for i in range(20):
        rt.append(
            (
                f"RENAME TABLE 到后缀 _r{i}",
                f"RENAME TABLE `{{TEST_TABLE_NAME}}` TO `{{TEST_TABLE_NAME}}_r{i}`;",
                tuple(["DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r0`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r1`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r2`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r3`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r4`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r5`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r6`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r7`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r8`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r9`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r10`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r11`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r12`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r13`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r14`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r15`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r16`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r17`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r18`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r19`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r20`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r21`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r22`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r23`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r24`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r25`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r26`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r27`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r28`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r29`;"])
            )
        )
    # Too many drops - simplify: use single suffix `{{TEST_TABLE_NAME}}_rn` for all rename cases
    simple_rn_extra = ("DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_rn`;",)
    rt = [
        item("测试将表重命名为 test_table_r01 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r01`;", tail=("DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r01`;",)),
        item("测试空表场景下将表重命名为 test_table_r02 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r02`;", tail=("TRUNCATE TABLE `{{TEST_TABLE_NAME}}`;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r02`;")),
        item("测试有单列索引时将表重命名为 test_table_r03 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r03`;", tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rn_varchar` (`varchar_col`);", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r03`;")),
        item("测试有联合索引时将表重命名为 test_table_r04 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r04`;", tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rn_multi` (`year_col`, `unsigned_decimal_col`);", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r04`;")),
        item("测试更新数据后将表重命名为 test_table_r05 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r05`;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_rn');", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r05`;")),
        item("测试删除部分数据后将表重命名为 test_table_r06 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r06`;", tail=("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 2 = 0;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r06`;")),
        item("测试插入额外数据后将表重命名为 test_table_r07 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r07`;", tail=("INSERT INTO `{{TEST_TABLE_NAME}}` (`int_col`,`varchar_col`,`enum_col`,`set_col`) VALUES (201,'rn_a','aaa','111'),(202,'rn_b','bbb','222');", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r07`;")),
        item("测试有唯一索引时将表重命名为 test_table_r08 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r08`;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col` WHERE `unsigned_int_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_rn_unique` (`unsigned_int_col`);", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r08`;")),
        item("测试有不可见索引时将表重命名为 test_table_r09 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r09`;", tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rn_invisible` (`varchar_col`) INVISIBLE;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r09`;")),
        item("测试更新时间列后将表重命名为 test_table_r10 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r10`;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2024-03-03 03:03:03.123456' WHERE `id_col` % 2 = 1;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r10`;")),
        item("测试更新文本列后将表重命名为 test_table_r11 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r11`;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `text_col` = CONCAT(COALESCE(`text_col`, ''), 'rename_text') WHERE `id_col` % 4 = 0;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r11`;")),
        item("测试更新二进制列后将表重命名为 test_table_r12 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r12`;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `binary_col` = x'42', `varbinary_col` = x'4344' WHERE `id_col` % 3 = 2;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r12`;")),
        item("测试存在主键空洞时将表重命名为 test_table_r13 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r13`;", tail=("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` IN (1,3,5,7,9);", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r13`;")),
        item("测试枚举集合列更新后将表重命名为 test_table_r14 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r14`;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'bbb', `set_col` = '111,222' WHERE `id_col` % 3 = 1;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r14`;")),
        item("测试目标表已存在时将表重命名为 test_table_r15 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r15`;", tail=("DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r15`;", "CREATE TABLE `{{TEST_TABLE_NAME}}_r15` LIKE `{{BASE_TABLE_NAME}}`;")),
        item("测试目标表名较长时将表重命名为 test_table_rename_case_16 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_rename_case_16`;", tail=("DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_rename_case_16`;",)),
        item("测试有多个辅助索引时将表重命名为 test_table_r17 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r17`;", tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rn_a` (`varchar_col`), ADD INDEX `idx_rn_b` (`date_col`), ADD INDEX `idx_rn_c` (`bit_col`);", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r17`;")),
        item("测试删除大部分数据后将表重命名为 test_table_r18 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r18`;", tail=("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 10 <> 0;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r18`;")),
        item("测试组合更新删除后将表重命名为 test_table_r19 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r19`;", tail=("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_combo');", "DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 5 = 0;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r19`;")),
        item("测试最终场景下将表重命名为 test_table_r20 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME TO `{{TEST_TABLE_NAME}}_r20`;", tail=("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rn_final` (`date_col`,`time_col`);", "UPDATE `{{TEST_TABLE_NAME}}` SET `date_col` = '2024-04-04', `time_col` = '04:04:04' WHERE `id_col` % 4 = 0;", "DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_r20`;")),
    ]
    write_many("rename_table", rt)

    # 13-15 maintenance
    opt = [
        ("测试普通数据量下执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ()),
        ("测试空表执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("TRUNCATE TABLE `{{TEST_TABLE_NAME}}`;",)),
        ("测试有单列索引时执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_opt_varchar` (`varchar_col`);",)),
        ("测试有联合索引时执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_opt_multi` (`year_col`, `unsigned_decimal_col`);",)),
        ("测试更新变长字符串后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_opt');",)),
        ("测试删除部分行后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 2 = 0;",)),
        ("测试更新并删除数据后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('u_', COALESCE(`varchar_col`, '')) WHERE `id_col` % 3 = 0;", "DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 5 = 0;")),
        ("测试插入额外行后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("INSERT INTO `{{TEST_TABLE_NAME}}` (`int_col`,`varchar_col`,`enum_col`,`set_col`) VALUES (101,'opt_a','aaa','111'),(102,'opt_b','bbb','222');",)),
        ("测试更新文本列后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `text_col` = CONCAT(COALESCE(`text_col`, ''), 'opt_text') WHERE `id_col` % 4 = 0;",)),
        ("测试更新 blob 列后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `blob_col` = CONCAT(COALESCE(`blob_col`, x''), x'41') WHERE `id_col` % 4 = 1;",)),
        ("测试有唯一索引时执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col` WHERE `unsigned_int_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_opt_unique_uint` (`unsigned_int_col`);")),
        ("测试有不可见索引时执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_opt_invisible` (`varchar_col`) INVISIBLE;",)),
        ("测试多次更新同一列后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = RPAD(COALESCE(`varchar_col`, ''), 40, 'x');", "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = TRIM(TRAILING 'x' FROM COALESCE(`varchar_col`, ''));")),
        ("测试更新时间列后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2024-01-01 00:00:00.123456' WHERE `id_col` % 2 = 1;",)),
        ("测试枚举集合列更新后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'bbb', `set_col` = '111,222' WHERE `id_col` % 3 = 1;",)),
        ("测试二进制列更新后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `binary_col` = x'42', `varbinary_col` = x'4344' WHERE `id_col` % 3 = 2;",)),
        ("测试存在主键空洞时执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` IN (1,3,5,7,9);",)),
        ("测试删除大部分行后执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 10 <> 0;",)),
        ("测试有索引且有更新删除时执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_opt_combo` (`varchar_col`);", "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_combo');", "DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 5 = 0;")),
        ("测试最终场景下执行 OPTIMIZE TABLE 的情况", "OPTIMIZE TABLE `{{TEST_TABLE_NAME}}`;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_opt_final` (`date_col`,`time_col`);", "UPDATE `{{TEST_TABLE_NAME}}` SET `date_col` = '2024-02-02', `time_col` = '02:02:02' WHERE `id_col` % 4 = 0;")),
    ]
    write_many("optimize_table", opt)

    force = [
        ("测试普通数据量下执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ()),
        ("测试空表执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("TRUNCATE TABLE `{{TEST_TABLE_NAME}}`;",)),
        ("测试有单列索引时执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_force_varchar` (`varchar_col`);",)),
        ("测试有联合索引时执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_force_multi` (`year_col`, `unsigned_decimal_col`);",)),
        ("测试更新变长字符串后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_force');",)),
        ("测试删除部分行后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 2 = 0;",)),
        ("测试更新并删除数据后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('f_', COALESCE(`varchar_col`, '')) WHERE `id_col` % 3 = 0;", "DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 5 = 0;")),
        ("测试插入额外行后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("INSERT INTO `{{TEST_TABLE_NAME}}` (`int_col`,`varchar_col`,`enum_col`,`set_col`) VALUES (301,'force_a','aaa','111'),(302,'force_b','bbb','222');",)),
        ("测试更新文本列后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `text_col` = CONCAT(COALESCE(`text_col`, ''), 'force_text') WHERE `id_col` % 4 = 0;",)),
        ("测试更新 blob 列后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `blob_col` = CONCAT(COALESCE(`blob_col`, x''), x'41') WHERE `id_col` % 4 = 1;",)),
        ("测试有唯一索引时执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col` WHERE `unsigned_int_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_force_unique_uint` (`unsigned_int_col`);")),
        ("测试有不可见索引时执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_force_invisible` (`varchar_col`) INVISIBLE;",)),
        ("测试多次更新同一列后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = RPAD(COALESCE(`varchar_col`, ''), 40, 'y');", "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = TRIM(TRAILING 'y' FROM COALESCE(`varchar_col`, ''));")),
        ("测试更新时间列后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2024-05-05 05:05:05.123456' WHERE `id_col` % 2 = 1;",)),
        ("测试枚举集合列更新后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'bbb', `set_col` = '111,222' WHERE `id_col` % 3 = 1;",)),
        ("测试二进制列更新后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `binary_col` = x'42', `varbinary_col` = x'4344' WHERE `id_col` % 3 = 2;",)),
        ("测试存在主键空洞时执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` IN (1,3,5,7,9);",)),
        ("测试删除大部分行后执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 10 <> 0;",)),
        ("测试有索引且有更新删除时执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_force_combo` (`varchar_col`);", "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_combo');", "DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 5 = 0;")),
        ("测试最终场景下执行 ALTER TABLE FORCE 的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` FORCE;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_force_final` (`date_col`,`time_col`);", "UPDATE `{{TEST_TABLE_NAME}}` SET `date_col` = '2024-06-06', `time_col` = '06:06:06' WHERE `id_col` % 4 = 0;")),
    ]
    write_many("alter_table_force", force)

    eng = [
        ("测试普通数据量下执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ()),
        ("测试空表执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("TRUNCATE TABLE `{{TEST_TABLE_NAME}}`;",)),
        ("测试有单列索引时执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_eng_varchar` (`varchar_col`);",)),
        ("测试有联合索引时执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_eng_multi` (`year_col`, `unsigned_decimal_col`);",)),
        ("测试更新变长字符串后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_eng');",)),
        ("测试删除部分行后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 2 = 0;",)),
        ("测试更新并删除数据后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('e_', COALESCE(`varchar_col`, '')) WHERE `id_col` % 3 = 0;", "DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 5 = 0;")),
        ("测试插入额外行后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("INSERT INTO `{{TEST_TABLE_NAME}}` (`int_col`,`varchar_col`,`enum_col`,`set_col`) VALUES (401,'eng_a','aaa','111'),(402,'eng_b','bbb','222');",)),
        ("测试更新文本列后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `text_col` = CONCAT(COALESCE(`text_col`, ''), 'eng_text') WHERE `id_col` % 4 = 0;",)),
        ("测试更新 blob 列后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `blob_col` = CONCAT(COALESCE(`blob_col`, x''), x'41') WHERE `id_col` % 4 = 1;",)),
        ("测试有唯一索引时执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col` WHERE `unsigned_int_col` IS NULL;", "ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_eng_unique_uint` (`unsigned_int_col`);")),
        ("测试有不可见索引时执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_eng_invisible` (`varchar_col`) INVISIBLE;",)),
        ("测试多次更新同一列后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = RPAD(COALESCE(`varchar_col`, ''), 40, 'z');", "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = TRIM(TRAILING 'z' FROM COALESCE(`varchar_col`, ''));")),
        ("测试更新时间列后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = '2024-07-07 07:07:07.123456' WHERE `id_col` % 2 = 1;",)),
        ("测试枚举集合列更新后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `enum_col` = 'bbb', `set_col` = '111,222' WHERE `id_col` % 3 = 1;",)),
        ("测试二进制列更新后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("UPDATE `{{TEST_TABLE_NAME}}` SET `binary_col` = x'42', `varbinary_col` = x'4344' WHERE `id_col` % 3 = 2;",)),
        ("测试存在主键空洞时执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` IN (1,3,5,7,9);",)),
        ("测试删除大部分行后执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 10 <> 0;",)),
        ("测试有索引且有更新删除时执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_eng_combo` (`varchar_col`);", "UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(COALESCE(`varchar_col`, ''), '_combo');", "DELETE FROM `{{TEST_TABLE_NAME}}` WHERE `id_col` % 5 = 0;")),
        ("测试最终场景下执行 ENGINE=InnoDB 空重建的情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` ENGINE=InnoDB;", ("ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_eng_final` (`date_col`,`time_col`);", "UPDATE `{{TEST_TABLE_NAME}}` SET `date_col` = '2024-08-08', `time_col` = '08:08:08' WHERE `id_col` % 4 = 0;")),
    ]
    write_many("alter_engine_innodb", eng)

    # 16) Converting a character set
    conv = [
        ("测试将表转换为 utf8mb4 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4;", ()),
        ("测试将表转换为 utf8mb4 且排序规则为 utf8mb4_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;", ()),
        ("测试将表转换为 utf8mb4 且排序规则为 utf8mb4_general_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;", ()),
        ("测试将表转换为 utf8mb4 且排序规则为 utf8mb4_unicode_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;", ()),
        ("测试将表转换为 utf8mb4 且排序规则为 utf8mb4_0900_ai_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;", ()),
        ("测试将表转换为 utf8mb4 且排序规则为 utf8mb4_0900_as_cs 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_cs;", ()),
        ("测试将表转换为 utf8mb3 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb3;", ()),
        ("测试将表转换为 utf8mb3 且排序规则为 utf8mb3_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb3 COLLATE utf8mb3_bin;", ()),
        ("测试将表转换为 utf8mb3 且排序规则为 utf8mb3_general_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci;", ()),
        ("测试将表转换为 latin1 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET latin1;", ()),
        ("测试将表转换为 latin1 且排序规则为 latin1_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET latin1 COLLATE latin1_bin;", ()),
        ("测试将表转换为 latin1 且排序规则为 latin1_swedish_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET latin1 COLLATE latin1_swedish_ci;", ()),
        ("测试将表转换为 ascii 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET ascii;", ()),
        ("测试将表转换为 ascii 且排序规则为 ascii_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET ascii COLLATE ascii_bin;", ()),
        ("测试将表转换为 ascii 且排序规则为 ascii_general_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET ascii COLLATE ascii_general_ci;", ()),
        ("测试将表转换为 gbk 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET gbk;", ()),
        ("测试将表转换为 gbk 且排序规则为 gbk_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET gbk COLLATE gbk_bin;", ()),
        ("测试将表转换为 gbk 且排序规则为 gbk_chinese_ci 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET gbk COLLATE gbk_chinese_ci;", ()),
        ("测试将表转换为 utf8mb4 且排序规则为 utf8mb4_0900_bin 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin;", ()),
        ("测试将表最终转换为 utf8mb4 的执行情况", "ALTER TABLE `{{TEST_TABLE_NAME}}` CONVERT TO CHARACTER SET utf8mb4;", ()),
    ]
    assert len(conv) == 20
    write_many("alter_convert_charset", conv)

    write_dml_insert_cases()
    write_dml_update_cases()

    print("Wrote new case directories under", OUT)


if __name__ == "__main__":
    main()
