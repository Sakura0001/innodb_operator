-- ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `float_col` float unsigned AFTER `double_col`;
-- 测试使用 MODIFY 将 float_col 调整到 double_col 之后的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `float_col` float unsigned AFTER `double_col`;
-- @TIMER_END
