-- CREATE INDEX `idx_year_unsigned_decimal` ON `{{TEST_TABLE_NAME}}` ((CAST(`year_col` AS UNSIGNED)), `unsigned_decimal_col`, `datetime_col`) ENGINE_ATTRIBUTE='{}' SECONDARY_ENGINE_ATTRIBUTE='{}';
-- 测试表达式列与无符号 decimal、datetime 列及引擎属性组合建立CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_year_unsigned_decimal` ON `{{TEST_TABLE_NAME}}` ((CAST(`year_col` AS UNSIGNED)), `unsigned_decimal_col`, `datetime_col`) ENGINE_ATTRIBUTE='{}' SECONDARY_ENGINE_ATTRIBUTE='{}';
-- @TIMER_END
