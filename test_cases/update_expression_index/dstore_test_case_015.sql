-- UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CASE WHEN `bigint_col` IS NULL THEN NULL WHEN `bigint_col` >= 0 THEN `bigint_col` ELSE -`bigint_col` END;
-- 测试表达式索引下 CASE 将 bigint_col 全部变正数的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_expr` ((ABS(`bigint_col`)));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = CASE WHEN `bigint_col` IS NULL THEN NULL WHEN `bigint_col` >= 0 THEN `bigint_col` ELSE -`bigint_col` END;
-- @TIMER_END
