-- ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;
-- 测试向 enum_col 末尾追加 3 个成员的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `enum_col` enum('aaa','bbb','ccc','ddd','eee','fff') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL;
-- @TIMER_END
