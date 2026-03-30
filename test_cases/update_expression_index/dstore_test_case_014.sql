-- UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = IF(`bigint_col` > 0, 1, 0) WHERE `bigint_col` IS NOT NULL;
-- 测试表达式索引下 UPDATE bool_col IF(bigint_col>0) WHERE bigint_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_expr` ((ABS(`bigint_col`)));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bool_col` = IF(`bigint_col` > 0, 1, 0) WHERE `bigint_col` IS NOT NULL;
-- @TIMER_END
