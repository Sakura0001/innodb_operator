-- CREATE INDEX `idx_int_bigint` ON `{{TEST_TABLE_NAME}}` (`int_col`, `bigint_col`);
-- 测试整数列组合建立CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_int_bigint` ON `{{TEST_TABLE_NAME}}` (`int_col`, `bigint_col`);
-- @TIMER_END
