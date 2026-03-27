-- CREATE INDEX `idx_bit_timestamp` ON `{{TEST_TABLE_NAME}}` (`bit_col`, `timestamp_col` DESC);
-- 测试 bit 与 timestamp 列组合建立CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_bit_timestamp` ON `{{TEST_TABLE_NAME}}` (`bit_col`, `timestamp_col` DESC);
-- @TIMER_END
