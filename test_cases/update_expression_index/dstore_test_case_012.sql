-- UPDATE `{{TEST_TABLE_NAME}}` SET `smallint_col` = CAST(`bigint_col` % 32767 AS SIGNED) WHERE `bigint_col` IS NOT NULL;
-- 测试表达式索引下 UPDATE smallint_col = bigint_col 取模 WHERE bigint_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_expr` ((ABS(`bigint_col`)));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `smallint_col` = CAST(`bigint_col` % 32767 AS SIGNED) WHERE `bigint_col` IS NOT NULL;
-- @TIMER_END
