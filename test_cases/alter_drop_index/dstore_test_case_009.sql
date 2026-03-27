-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_multi_a`;
-- 测试存在多个索引时删除其中一个索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_drop_multi_a` (`varchar_col`), ADD INDEX `idx_drop_multi_b` (`char_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_multi_a`;
-- @TIMER_END
