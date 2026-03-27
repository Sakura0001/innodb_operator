-- CREATE INDEX `idx_tiny_bool` ON `{{TEST_TABLE_NAME}}` (`tinyint_col`, `bool_col`);
-- 测试 tinyint 与 bool 列组合CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_tiny_bool` ON `{{TEST_TABLE_NAME}}` (`tinyint_col`, `bool_col`);
-- @TIMER_END
