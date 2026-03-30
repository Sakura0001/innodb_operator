-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = RPAD(COALESCE(`varchar_col`, '_'), 64, 'z') WHERE `id_col` % 3 = 0;
-- 测试前缀索引下 UPDATE 索引列 RPAD 填充 WHERE id_col 模3 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_prefix` (`varchar_col`(32));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = RPAD(COALESCE(`varchar_col`, '_'), 64, 'z') WHERE `id_col` % 3 = 0;
-- @TIMER_END
