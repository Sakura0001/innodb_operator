-- UPDATE `{{TEST_TABLE_NAME}}` SET `set_col` = '111,222', `enum_col` = 'ccc' WHERE `id_col` % 11 = 0;
-- 测试仅主键下 UPDATE set_col + enum_col WHERE id_col % 11 = 0 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `set_col` = '111,222', `enum_col` = 'ccc' WHERE `id_col` % 11 = 0;
-- @TIMER_END
