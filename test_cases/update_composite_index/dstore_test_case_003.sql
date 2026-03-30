-- UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 3 WHERE `year_col` = 2024 AND `int_col` = 0 AND `varchar_col` LIKE 'c_%';
-- 测试组合索引下 UPDATE WHERE 三列全匹配含 varchar LIKE 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 3 WHERE `year_col` = 2024 AND `int_col` = 0 AND `varchar_col` LIKE 'c_%';
-- @TIMER_END
