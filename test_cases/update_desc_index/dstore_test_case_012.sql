-- UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 42 WHERE `varchar_col` BETWEEN 'a' AND 'm';
-- 测试逆序索引 varchar_col DESC 下 UPDATE int_col WHERE varchar_col BETWEEN 范围的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_desc_vc` (`varchar_col` DESC);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 42 WHERE `varchar_col` BETWEEN 'a' AND 'm';
-- @TIMER_END
