-- UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = YEAR(`date_col`) WHERE `year_col` BETWEEN 2020 AND 2030 AND `date_col` IS NOT NULL;
-- 测试组合索引下 UPDATE 首列 year_col 为派生表达式 WHERE year_col 范围的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = YEAR(`date_col`) WHERE `year_col` BETWEEN 2020 AND 2030 AND `date_col` IS NOT NULL;
-- @TIMER_END
