-- UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `varchar_col` LIKE '%0%';
-- 测试逆序索引 varchar_col DESC 下 UPDATE bool_col WHERE varchar_col LIKE 含数字的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_desc_vc` (`varchar_col` DESC);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `varchar_col` LIKE '%0%';
-- @TIMER_END
