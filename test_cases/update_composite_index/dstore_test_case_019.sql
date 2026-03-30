-- UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = NULL, `int_col` = NULL WHERE `id_col` % 7 = 0;
-- 测试组合索引下将 year_col, int_col 同时设为 NULL WHERE id_col 模7 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = NULL, `int_col` = NULL WHERE `id_col` % 7 = 0;
-- @TIMER_END
