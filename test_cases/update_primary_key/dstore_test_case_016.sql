-- UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1, `tinyint_col` = 100 WHERE `id_col` % 7 = 0;
-- 测试仅主键下 UPDATE 两非索引列 WHERE id_col % 7 = 0 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1, `tinyint_col` = 100 WHERE `id_col` % 7 = 0;
-- @TIMER_END
