-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_decimal_time`;
-- 测试删除 unsigned decimal 与 time 组合索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_drop_decimal_time` (`unsigned_decimal_col`, `time_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_decimal_time`;
-- @TIMER_END
