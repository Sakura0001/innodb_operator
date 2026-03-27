-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_medium_longtext` (`mediumtext_col`(40), `longtext_col`(60));
-- 测试 mediumtext 与 longtext 前缀列组合建立索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_medium_longtext` (`mediumtext_col`(40), `longtext_col`(60));
-- @TIMER_END
