-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_unique_old` TO `idx_rename_unique_new`;
-- 测试重命名唯一索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`varchar_col`) VALUES ('rn_u1'), ('rn_u2');
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_rename_unique_old` (`varchar_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_unique_old` TO `idx_rename_unique_new`;
-- @TIMER_END
