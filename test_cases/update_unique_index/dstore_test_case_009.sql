-- UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = CAST(`unsigned_int_col` % 1000 AS SIGNED) WHERE `unsigned_int_col` IS NOT NULL;
-- 测试唯一索引下 UPDATE int_col = unsigned_int_col 取模 WHERE unsigned_int_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_upd_uq_uint` (`unsigned_int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = CAST(`unsigned_int_col` % 1000 AS SIGNED) WHERE `unsigned_int_col` IS NOT NULL;
-- @TIMER_END
