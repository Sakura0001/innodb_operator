-- ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin AFTER `mediumtext_col`;
-- 测试使用 MODIFY 将 enum_col 调整到 mediumtext_col 之后的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin AFTER `mediumtext_col`;
-- @TIMER_END
