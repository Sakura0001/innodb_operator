-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_text_long`;
-- 测试删除 mediumtext 与 longtext 前缀组合索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_drop_text_long` (`mediumtext_col`(20), `longtext_col`(20));
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_text_long`;
-- @TIMER_END
