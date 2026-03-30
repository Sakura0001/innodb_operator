-- UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` + 1000 WHERE `int_col` IS NOT NULL;
-- 测试单列索引 int_col 下 UPDATE bigint_col WHERE int_col IS NOT NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_single_int` (`int_col`);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `bigint_col` = `bigint_col` + 1000 WHERE `int_col` IS NOT NULL;
-- @TIMER_END
