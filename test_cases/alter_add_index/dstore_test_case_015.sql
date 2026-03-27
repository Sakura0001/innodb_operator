-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_year_unsigned` (`year_col`, `unsigned_decimal_col` DESC);
-- 测试 year 与 unsigned decimal 列组合建立索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_year_unsigned` (`year_col`, `unsigned_decimal_col` DESC);
-- @TIMER_END
