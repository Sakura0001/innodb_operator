-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CASE WHEN `int_col` > 0 THEN 'pos' WHEN `int_col` < 0 THEN 'neg' ELSE 'zero' END WHERE `int_col` IS NOT NULL;
-- 测试单列索引 int_col 下 CASE 表达式 UPDATE varchar_col WHERE int_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_single_int` (`int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CASE WHEN `int_col` > 0 THEN 'pos' WHEN `int_col` < 0 THEN 'neg' ELSE 'zero' END WHERE `int_col` IS NOT NULL;
-- @TIMER_END
