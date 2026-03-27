-- CREATE FULLTEXT INDEX `idx_ft_varchar_text` ON `{{TEST_TABLE_NAME}}` (`varchar_col`, `text_col`) COMMENT 'ft_varchar_text';
-- 测试 varchar 与 text 列组合CREATE FULLTEXT INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE FULLTEXT INDEX `idx_ft_varchar_text` ON `{{TEST_TABLE_NAME}}` (`varchar_col`, `text_col`) COMMENT 'ft_varchar_text';
-- @TIMER_END
