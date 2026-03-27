-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT INDEX `idx_ft_longtext` (`longtext_col`) COMMENT 'ft_longtext';
-- 测试单列 longtext FULLTEXT 索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT INDEX `idx_ft_longtext` (`longtext_col`) COMMENT 'ft_longtext';
-- @TIMER_END
