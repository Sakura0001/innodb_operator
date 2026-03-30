-- UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2025, `int_col` = 0 WHERE `id_col` IN (1, 2, 3, 4, 5);
-- 测试组合索引下同时 UPDATE 多个索引列 WHERE id_col IN 少量主键的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `year_col` = 2025, `int_col` = 0 WHERE `id_col` IN (1, 2, 3, 4, 5);
-- @TIMER_END
