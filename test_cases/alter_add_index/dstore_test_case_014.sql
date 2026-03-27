-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_tiny_bool` (`tinyint_col`, `bool_col`);
-- 测试 tinyint 与 bool 列组合建立索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_tiny_bool` (`tinyint_col`, `bool_col`);
-- @TIMER_END
