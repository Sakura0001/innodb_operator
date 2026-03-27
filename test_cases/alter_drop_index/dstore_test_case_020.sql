-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP KEY `idx_drop_created_renamed`;
-- 测试删除由 CREATE INDEX 创建并重命名后的索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
CREATE INDEX `idx_drop_created_old` ON `{{TEST_TABLE_NAME}}` (`varchar_col`);
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_drop_created_old` TO `idx_drop_created_renamed`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP KEY `idx_drop_created_renamed`;
-- @TIMER_END
