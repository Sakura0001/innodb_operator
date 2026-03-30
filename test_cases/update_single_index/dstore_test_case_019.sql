-- UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = ABS(`int_col`) WHERE `int_col` < 0;
-- 测试单列索引 int_col 下将负 int_col 取绝对值 UPDATE 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_single_int` (`int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = ABS(`int_col`) WHERE `int_col` < 0;
-- @TIMER_END
