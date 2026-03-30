-- UPDATE `{{TEST_TABLE_NAME}}` SET `decimal_col` = CAST(`unsigned_int_col` AS DECIMAL(25,5)) * 0.01 WHERE `unsigned_int_col` BETWEEN 100 AND 10000;
-- 测试唯一索引下 UPDATE decimal_col WHERE unsigned_int_col BETWEEN 小额区间的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_upd_uq_uint` (`unsigned_int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `decimal_col` = CAST(`unsigned_int_col` AS DECIMAL(25,5)) * 0.01 WHERE `unsigned_int_col` BETWEEN 100 AND 10000;
-- @TIMER_END
