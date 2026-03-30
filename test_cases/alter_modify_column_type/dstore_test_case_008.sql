-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `decimal_col` `decimal_col` decimal(30,10) unsigned;
-- 测试将 decimal_col 从 decimal(25,5) unsigned 改为 decimal(30,10) unsigned 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `decimal_col` `decimal_col` decimal(30,10) unsigned;
-- @TIMER_END
