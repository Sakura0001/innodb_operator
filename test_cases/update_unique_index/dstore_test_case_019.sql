-- UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = DATE_ADD(COALESCE(`datetime_col`, NOW()), INTERVAL CAST(`unsigned_int_col` % 3600 AS UNSIGNED) SECOND) WHERE `unsigned_int_col` < 100;
-- 测试唯一索引下 UPDATE datetime_col 加秒偏移 WHERE unsigned_int_col < 100 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_upd_uq_uint` (`unsigned_int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `datetime_col` = DATE_ADD(COALESCE(`datetime_col`, NOW()), INTERVAL CAST(`unsigned_int_col` % 3600 AS UNSIGNED) SECOND) WHERE `unsigned_int_col` < 100;
-- @TIMER_END
