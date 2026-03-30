-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `tinyint_col` `tinyint_col` tinyint unsigned AFTER `smallint_col`;
-- 测试使用 CHANGE 将 tinyint_col 调整到 smallint_col 之后的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `tinyint_col` `tinyint_col` tinyint unsigned AFTER `smallint_col`;
-- @TIMER_END
