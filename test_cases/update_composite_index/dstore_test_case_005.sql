-- UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `year_col` IS NOT NULL AND `int_col` > 0;
-- 测试组合索引下 UPDATE WHERE year_col IS NOT NULL AND int_col > 0 复合条件的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = 1 WHERE `year_col` IS NOT NULL AND `int_col` > 0;
-- @TIMER_END
