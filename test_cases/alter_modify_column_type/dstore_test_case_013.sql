-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `timestamp_col` `timestamp_col` datetime DEFAULT NULL;
-- 测试将 timestamp_col 从 timestamp 改为 datetime 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `timestamp_col` `timestamp_col` datetime DEFAULT NULL;
-- @TIMER_END
