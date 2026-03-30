-- UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = `int_col` + 100 WHERE `year_col` = 2024;
-- 测试组合索引下 UPDATE 第二列 int_col WHERE year_col 精确匹配的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = `int_col` + 100 WHERE `year_col` = 2024;
-- @TIMER_END
