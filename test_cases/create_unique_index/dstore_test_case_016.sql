-- CREATE UNIQUE INDEX `idx_unique_date_datetime` ON `{{TEST_TABLE_NAME}}` (`date_col`, `datetime_col`);
-- 测试 date 与 datetime 列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`date_col`, `datetime_col`) VALUES ('2024-05-01', '2024-05-01 10:00:00.000000'), ('2024-05-02', '2024-05-02 10:00:00.000000');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_date_datetime` ON `{{TEST_TABLE_NAME}}` (`date_col`, `datetime_col`);
-- @TIMER_END
