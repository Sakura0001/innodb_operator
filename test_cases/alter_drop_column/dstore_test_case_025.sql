-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP CHECK `chk_drop_col_multi_ok`, DROP COLUMN `int_col`;
-- 测试同一语句先删除多列 CHECK 约束再删除列的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD CONSTRAINT `chk_drop_col_multi_ok` CHECK (`int_col` IS NULL OR `bigint_col` IS NULL OR `int_col` <= `bigint_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP CHECK `chk_drop_col_multi_ok`, DROP COLUMN `int_col`;
-- @TIMER_END
