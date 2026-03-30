-- UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `varchar_col` = 'c_0000000001';
-- 测试前缀索引 varchar_col(32) 下 UPDATE 非索引列 WHERE varchar_col 精确匹配的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_prefix` (`varchar_col`(32));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0 WHERE `varchar_col` = 'c_0000000001';
-- @TIMER_END
