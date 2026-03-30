-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('u_', LPAD(`id_col`, 10, '0'));
-- 测试唯一索引下全表 UPDATE 非唯一列 varchar_col 无 WHERE 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
UPDATE `{{TEST_TABLE_NAME}}` SET `unsigned_int_col` = `id_col`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_upd_uq_uint` (`unsigned_int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('u_', LPAD(`id_col`, 10, '0'));
-- @TIMER_END
