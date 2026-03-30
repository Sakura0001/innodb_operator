-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `float_col` `float_col` double unsigned;
-- 测试将 float_col 从 float unsigned 改为 double unsigned 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `float_col` `float_col` double unsigned;
-- @TIMER_END
