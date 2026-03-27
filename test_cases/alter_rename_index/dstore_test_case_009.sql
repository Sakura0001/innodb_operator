-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_after_create_old` TO `idx_rename_after_create_new`;
-- 测试由 CREATE INDEX 创建的索引再被重命名的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
CREATE INDEX `idx_rename_after_create_old` ON `{{TEST_TABLE_NAME}}` (`varchar_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_after_create_old` TO `idx_rename_after_create_new`;
-- @TIMER_END
