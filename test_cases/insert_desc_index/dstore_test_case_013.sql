-- INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `bigint_col`;
-- 测试逆序索引 varchar_col DESC 下从 C 插入5万行 ORDER BY bigint_col 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}_src`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_insert_desc_vc` (`varchar_col` DESC);
CREATE TABLE `{{TEST_TABLE_NAME}}_src` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}_src` (`id_col`, `int_col`, `bigint_col`, `year_col`, `char_col`, `tinyint_col`, `bool_col`, `smallint_col`, `mediumint_col`, `decimal_col`, `float_col`, `double_col`, `date_col`, `datetime_col`, `timestamp_col`, `time_col`, `varchar_col`, `binary_col`, `varbinary_col`, `tinyblob_col`, `blob_col`, `mediumblob_col`, `longblob_col`, `tinytext_col`, `text_col`, `mediumtext_col`, `longtext_col`, `enum_col`, `set_col`, `bit_col`, `unsigned_int_col`, `unsigned_decimal_col`)
SELECT 16800000 + nums.n AS `id_col`, s.`int_col`, s.`bigint_col`, s.`year_col`, s.`char_col`, s.`tinyint_col`, s.`bool_col`, s.`smallint_col`, s.`mediumint_col`, s.`decimal_col`, s.`float_col`, s.`double_col`, s.`date_col`, s.`datetime_col`, s.`timestamp_col`, s.`time_col`, s.`varchar_col` AS `varchar_col`, s.`binary_col`, s.`varbinary_col`, s.`tinyblob_col`, s.`blob_col`, s.`mediumblob_col`, s.`longblob_col`, s.`tinytext_col`, s.`text_col`, s.`mediumtext_col`, s.`longtext_col`, s.`enum_col`, s.`set_col`, s.`bit_col`, s.`unsigned_int_col` AS `unsigned_int_col`, s.`unsigned_decimal_col`
FROM (SELECT * FROM `{{BASE_TABLE_NAME}}` LIMIT 1) s
CROSS JOIN (SELECT a.N + b.N * 10 + c.N * 100 + d.N * 1000 + e.N * 10000 AS n
FROM (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a, (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b, (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c, (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) d, (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) e) nums
WHERE nums.n < 50000
-- @PREPARE_END

-- @TIMER_START
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{TEST_TABLE_NAME}}_src` ORDER BY `bigint_col`;
-- @TIMER_END
