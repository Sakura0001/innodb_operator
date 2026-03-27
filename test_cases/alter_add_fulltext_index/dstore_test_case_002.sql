-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT INDEX `idx_ft_varchar_text` (`varchar_col`, `text_col`) COMMENT 'ft_varchar_text';
-- 测试 varchar 与 text 列组合建立 FULLTEXT 索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT INDEX `idx_ft_varchar_text` (`varchar_col`, `text_col`) COMMENT 'ft_varchar_text';
-- @TIMER_END
