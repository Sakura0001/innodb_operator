-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `decimal_col` `decimal_col` decimal(25,5) unsigned AFTER `float_col`;
-- 测试使用 CHANGE 将 decimal_col 调整到 float_col 之后的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `decimal_col` `decimal_col` decimal(25,5) unsigned AFTER `float_col`;
-- @TIMER_END
