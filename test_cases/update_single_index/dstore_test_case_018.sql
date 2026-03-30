-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = UPPER(COALESCE(`varchar_col`, '')) WHERE `int_col` BETWEEN 0 AND 10000;
-- 测试单列索引 int_col 下 UPDATE varchar_col UPPER WHERE int_col 范围的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_single_int` (`int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = UPPER(COALESCE(`varchar_col`, '')) WHERE `int_col` BETWEEN 0 AND 10000;
-- @TIMER_END
