-- UPDATE `{{TEST_TABLE_NAME}}` SET `tinytext_col` = `varchar_col` WHERE `varchar_col` IS NOT NULL;
-- 测试前缀索引下 UPDATE tinytext_col 为 varchar_col WHERE varchar_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_prefix` (`varchar_col`(32));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `tinytext_col` = `varchar_col` WHERE `varchar_col` IS NOT NULL;
-- @TIMER_END
