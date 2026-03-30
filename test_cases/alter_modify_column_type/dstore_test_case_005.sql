-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `tinyint_col` `tinyint_col` smallint unsigned;
-- 测试将 tinyint_col 从 tinyint unsigned 改为 smallint unsigned 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `tinyint_col` `tinyint_col` smallint unsigned;
-- @TIMER_END
