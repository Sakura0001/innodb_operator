-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_text_prefix_old` TO `idx_rename_text_prefix_new`;
-- 测试重命名 text 前缀索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rename_text_prefix_old` (`text_col`(20));
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_text_prefix_old` TO `idx_rename_text_prefix_new`;
-- @TIMER_END
