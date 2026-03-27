-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_dup_name` (`varchar_col`);
-- 测试重复唯一索引名时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`varchar_col`) VALUES ('dup_name_a'), ('dup_name_b');
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_dup_name` (`char_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_dup_name` (`varchar_col`);
-- @TIMER_END
