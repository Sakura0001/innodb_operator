-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `float_col` `float_col_r1` float unsigned;
-- 测试使用 CHANGE 将 float_col 重命名为 float_col_r1 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `float_col` `float_col_r1` float unsigned;
-- @TIMER_END
