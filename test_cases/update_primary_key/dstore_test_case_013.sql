-- UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = -`id_col`, `varchar_col` = CONCAT('mult_', LPAD(`id_col`, 6, '0')) WHERE `id_col` % 3 = 0;
-- 测试仅主键下多列同时 UPDATE WHERE id_col % 3 = 0 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = -`id_col`, `varchar_col` = CONCAT('mult_', LPAD(`id_col`, 6, '0')) WHERE `id_col` % 3 = 0;
-- @TIMER_END
