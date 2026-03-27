-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_bit_timestamp` (`bit_col`, `timestamp_col` DESC);
-- 测试 bit 与 timestamp 列组合建立普通索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_bit_timestamp` (`bit_col`, `timestamp_col` DESC);
-- @TIMER_END
