-- CREATE UNIQUE INDEX `idx_unique_decimal_double` ON `{{TEST_TABLE_NAME}}` (`decimal_col`, `double_col`);
-- 测试 decimal 与 double 列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`decimal_col`, `double_col`) VALUES (11.10000, 101.1), (22.20000, 202.2);
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_decimal_double` ON `{{TEST_TABLE_NAME}}` (`decimal_col`, `double_col`);
-- @TIMER_END
