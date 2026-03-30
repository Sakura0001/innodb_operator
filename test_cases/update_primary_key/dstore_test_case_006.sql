-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('pk_', LPAD(`id_col`, 10, '0')) WHERE `id_col` % 2 = 0;
-- 测试仅主键下 UPDATE WHERE id_col % 2 = 0 半表的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('pk_', LPAD(`id_col`, 10, '0')) WHERE `id_col` % 2 = 0;
-- @TIMER_END
