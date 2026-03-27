-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_enum_date_time` (`enum_col`, `date_col`, `time_col` DESC);
-- 测试 enum、date、time 列组合建立普通索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_enum_date_time` (`enum_col`, `date_col`, `time_col` DESC);
-- @TIMER_END
