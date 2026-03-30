-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varbinary_col` `varbinary_col` binary(255);
-- 测试将 varbinary_col 从 varbinary(255) 改为 binary(255) 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varbinary_col` `varbinary_col` binary(255);
-- @TIMER_END
