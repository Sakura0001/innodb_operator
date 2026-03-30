-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bigint_col` `bigint_col` decimal(20,0);
-- 测试将 bigint_col 从 bigint 改为 decimal(20,0) 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `bigint_col` `bigint_col` decimal(20,0);
-- @TIMER_END
