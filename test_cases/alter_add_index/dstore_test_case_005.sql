-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_decimal_float_double` (`decimal_col`, `float_col`, `double_col`);
-- 测试 decimal、float、double 列组合建立普通索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_decimal_float_double` (`decimal_col`, `float_col`, `double_col`);
-- @TIMER_END
