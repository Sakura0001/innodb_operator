-- UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('c_', COALESCE(`varchar_col`, '')) WHERE `year_col` = 2024 AND `int_col` > 0;
-- 测试组合索引下 UPDATE 第三列 varchar_col WHERE 前两列匹配的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_comp` (`year_col`, `int_col`, `varchar_col`(16));
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `varchar_col` = CONCAT('c_', COALESCE(`varchar_col`, '')) WHERE `year_col` = 2024 AND `int_col` > 0;
-- @TIMER_END
