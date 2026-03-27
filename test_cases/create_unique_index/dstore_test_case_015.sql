-- CREATE UNIQUE INDEX `idx_unique_year_unsigned` ON `{{TEST_TABLE_NAME}}` (`year_col`, `unsigned_decimal_col`);
-- 测试 year 与 unsigned decimal 列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`year_col`, `unsigned_decimal_col`) VALUES (2022, 100), (2023, 200);
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_year_unsigned` ON `{{TEST_TABLE_NAME}}` (`year_col`, `unsigned_decimal_col`);
-- @TIMER_END
