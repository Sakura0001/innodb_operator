-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('new_', LPAD(`id_col`, 10, '0')) WHERE `id_col` % 5 = 0;
-- 测试前缀索引下 UPDATE 索引列为唯一拼接值 WHERE id_col 模5 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_prefix` (`varchar_col`(32));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('new_', LPAD(`id_col`, 10, '0')) WHERE `id_col` % 5 = 0;
-- @TIMER_END
