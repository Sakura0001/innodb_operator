-- UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = CAST(`unsigned_int_col` % 127 AS UNSIGNED) WHERE `unsigned_int_col` < 1000;
-- 测试唯一索引下 UPDATE tinyint_col WHERE unsigned_int_col < 1000 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_upd_uq_uint` (`unsigned_int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = CAST(`unsigned_int_col` % 127 AS UNSIGNED) WHERE `unsigned_int_col` < 1000;
-- @TIMER_END
