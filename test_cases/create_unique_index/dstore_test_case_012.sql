-- CREATE UNIQUE INDEX `idx_unique_decimal_time` ON `{{TEST_TABLE_NAME}}` (`unsigned_decimal_col`, `time_col` DESC);
-- 测试 unsigned decimal 与 time 列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`unsigned_decimal_col`, `time_col`) VALUES (101, '10:00:00'), (202, '11:00:00');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_decimal_time` ON `{{TEST_TABLE_NAME}}` (`unsigned_decimal_col`, `time_col` DESC);
-- @TIMER_END
