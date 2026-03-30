-- UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CAST(`int_col` AS SIGNED) * 1000, `mediumint_col` = ABS(`int_col`) % 8388607 WHERE `int_col` IS NOT NULL;
-- 测试表达式索引下 UPDATE bigint_col = int_col*1000 并 mediumint_col 同时更新的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_expr` ((ABS(`bigint_col`)));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CAST(`int_col` AS SIGNED) * 1000, `mediumint_col` = ABS(`int_col`) % 8388607 WHERE `int_col` IS NOT NULL;
-- @TIMER_END
