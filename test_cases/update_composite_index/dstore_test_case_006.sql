-- UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2025 WHERE `id_col` % 2 = 0;
-- 测试组合索引下 UPDATE 首列 year_col 本身 WHERE id_col 偶数的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2025 WHERE `id_col` % 2 = 0;
-- @TIMER_END
