-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_varbinary_binary` (`varbinary_col`(16), `binary_col`) COMMENT 'binary_index' VISIBLE;
-- 测试 varbinary 与 binary 列组合建立普通索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_varbinary_binary` (`varbinary_col`(16), `binary_col`) COMMENT 'binary_index' VISIBLE;
-- @TIMER_END
