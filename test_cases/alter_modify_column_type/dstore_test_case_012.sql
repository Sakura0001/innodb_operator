-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `datetime_col` `datetime_col` datetime(3);
-- 测试将 datetime_col 从 datetime(6) 改为 datetime(3) 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `datetime_col` `datetime_col` datetime(3);
-- @TIMER_END
