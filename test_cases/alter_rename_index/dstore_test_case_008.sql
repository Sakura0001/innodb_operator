-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_conflict_old` TO `idx_rename_conflict_new`;
-- 测试重命名索引到已存在名称时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rename_conflict_old` (`varchar_col`), ADD INDEX `idx_rename_conflict_new` (`char_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_conflict_old` TO `idx_rename_conflict_new`;
-- @TIMER_END
