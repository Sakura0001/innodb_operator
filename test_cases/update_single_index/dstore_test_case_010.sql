-- UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `id_col` IN (1, 2, 3, 4, 5);
-- 测试单列索引 int_col 下 UPDATE WHERE id_col IN 少量主键的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_single_int` (`int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `id_col` IN (1, 2, 3, 4, 5);
-- @TIMER_END
