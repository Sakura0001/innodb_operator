-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP KEY `idx_drop_after_rename_new`;
-- 测试重命名后的索引再被删除的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_drop_after_rename_old` (`varchar_col`);
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_drop_after_rename_old` TO `idx_drop_after_rename_new`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP KEY `idx_drop_after_rename_new`;
-- @TIMER_END
