-- UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = ABS(`bigint_col`) WHERE `bigint_col` < 0;
-- 测试表达式索引下 UPDATE 源列 bigint_col 取绝对值 WHERE bigint_col < 0 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_expr` ((ABS(`bigint_col`)));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = ABS(`bigint_col`) WHERE `bigint_col` < 0;
-- @TIMER_END
