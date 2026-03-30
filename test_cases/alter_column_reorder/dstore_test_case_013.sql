-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `timestamp_col` `timestamp_col` timestamp NULL DEFAULT NULL AFTER `datetime_col`;
-- 测试使用 CHANGE 将 timestamp_col 调整到 datetime_col 之后的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `timestamp_col` `timestamp_col` timestamp NULL DEFAULT NULL AFTER `datetime_col`;
-- @TIMER_END
