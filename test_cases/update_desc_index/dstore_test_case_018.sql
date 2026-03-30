-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = REPLACE(COALESCE(`varchar_col`, ''), '_', '-') WHERE `varchar_col` LIKE '%\_%';
-- 测试逆序索引 varchar_col DESC 下 UPDATE 索引列 REPLACE 替换字符 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_desc_vc` (`varchar_col` DESC);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = REPLACE(COALESCE(`varchar_col`, ''), '_', '-') WHERE `varchar_col` LIKE '%\_%';
-- @TIMER_END
