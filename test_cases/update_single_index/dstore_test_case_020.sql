-- UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1, `bool_col` = 1 WHERE `int_col` > 0 AND `varchar_col` IS NOT NULL;
-- 测试单列索引 int_col 下 UPDATE 多非索引列 WHERE int_col > 0 AND varchar_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_single_int` (`int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `tinyint_col` = 1, `bool_col` = 1 WHERE `int_col` > 0 AND `varchar_col` IS NOT NULL;
-- @TIMER_END
