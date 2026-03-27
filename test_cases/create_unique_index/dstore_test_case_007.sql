-- CREATE UNIQUE INDEX `idx_unique_datetime_timestamp` ON `{{TEST_TABLE_NAME}}` (`datetime_col`, `timestamp_col`);
-- 测试 datetime 与 timestamp 列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`datetime_col`, `timestamp_col`) VALUES ('2024-03-01 10:00:00.000000', '2024-03-01 10:00:00'), ('2024-03-02 11:00:00.000000', '2024-03-02 11:00:00');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_datetime_timestamp` ON `{{TEST_TABLE_NAME}}` (`datetime_col`, `timestamp_col`);
-- @TIMER_END
