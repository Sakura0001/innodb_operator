-- UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'dsc2' ORDER BY `year_col` DESC, `int_col` DESC LIMIT 200;
-- 测试组合索引下 UPDATE ORDER BY year_col DESC, int_col DESC LIMIT 200 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `char_col` = 'dsc2' ORDER BY `year_col` DESC, `int_col` DESC LIMIT 200;
-- @TIMER_END
