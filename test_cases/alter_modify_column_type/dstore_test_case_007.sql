-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `mediumint_col` `mediumint_col` bigint unsigned;
-- 测试将 mediumint_col 从 mediumint unsigned 改为 bigint unsigned 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `mediumint_col` `mediumint_col` bigint unsigned;
-- @TIMER_END
