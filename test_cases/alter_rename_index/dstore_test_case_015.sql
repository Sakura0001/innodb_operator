-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_unique_inv_old` TO `idx_rename_unique_inv_new`;
-- 测试重命名 INVISIBLE 唯一索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`varchar_col`) VALUES ('rui_a'), ('rui_b');
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_rename_unique_inv_old` (`varchar_col`) INVISIBLE;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_unique_inv_old` TO `idx_rename_unique_inv_new`;
-- @TIMER_END
