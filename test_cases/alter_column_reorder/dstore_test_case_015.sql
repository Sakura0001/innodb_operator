-- ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varchar_col` `varchar_col` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin AFTER `set_col`;
-- 测试使用 CHANGE 将 varchar_col 调整到 set_col 之后的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` CHANGE COLUMN `varchar_col` `varchar_col` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin AFTER `set_col`;
-- @TIMER_END
