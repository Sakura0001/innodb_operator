-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varbinary_col` `varbinary_col_r1` varbinary(255);
-- 测试使用 CHANGE 将 varbinary_col 重命名为 varbinary_col_r1 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varbinary_col` `varbinary_col_r1` varbinary(255);
-- @TIMER_END
