-- CREATE UNIQUE INDEX `idx_unique_binary_pair` ON `{{TEST_TABLE_NAME}}` (`varbinary_col`(16), `binary_col`);
-- 测试 varbinary 前缀列与 binary 列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`varbinary_col`, `binary_col`) VALUES ('a1', 'a'), ('b2', 'b');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_binary_pair` ON `{{TEST_TABLE_NAME}}` (`varbinary_col`(16), `binary_col`);
-- @TIMER_END
