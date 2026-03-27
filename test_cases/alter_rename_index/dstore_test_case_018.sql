-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_bit_ts_old` TO `idx_rename_bit_ts_new`;
-- 测试重命名 bit 与 timestamp 组合索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_rename_bit_ts_old` (`bit_col`, `timestamp_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_bit_ts_old` TO `idx_rename_bit_ts_new`;
-- @TIMER_END
