-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_text_year` (`text_col`(20), `year_col`);
-- 测试 text 前缀列与 year 列组合建立唯一索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`text_col`, `year_col`) VALUES ('text_year_a', 2023), ('text_year_b', 2024);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_text_year` (`text_col`(20), `year_col`);
-- @TIMER_END
