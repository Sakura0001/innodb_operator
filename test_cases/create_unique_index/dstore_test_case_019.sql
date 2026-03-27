-- CREATE UNIQUE INDEX `idx_unique_prefix_dup` ON `{{TEST_TABLE_NAME}}` (`varchar_col`(5));
-- 测试唯一前缀索引在前缀重复时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`varchar_col`) VALUES ('prefix_AAAAA_1'), ('prefix_AAAAA_2');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_prefix_dup` ON `{{TEST_TABLE_NAME}}` (`varchar_col`(5));
-- @TIMER_END
