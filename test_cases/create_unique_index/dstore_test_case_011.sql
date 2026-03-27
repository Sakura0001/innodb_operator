-- CREATE UNIQUE INDEX `idx_unique_missing_col` ON `{{TEST_TABLE_NAME}}` (`missing_col`);
-- 测试CREATE UNIQUE INDEX引用不存在列时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`varchar_col`) VALUES ('missing_a'), ('missing_b');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_missing_col` ON `{{TEST_TABLE_NAME}}` (`missing_col`);
-- @TIMER_END
