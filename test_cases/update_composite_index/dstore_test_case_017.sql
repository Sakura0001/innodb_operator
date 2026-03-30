-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(CAST(`year_col` AS CHAR), '_', CAST(`int_col` AS CHAR)) WHERE `year_col` IS NOT NULL;
-- 测试组合索引下 UPDATE varchar_col 为年份+整数拼接 WHERE year_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT(CAST(`year_col` AS CHAR), '_', CAST(`int_col` AS CHAR)) WHERE `year_col` IS NOT NULL;
-- @TIMER_END
