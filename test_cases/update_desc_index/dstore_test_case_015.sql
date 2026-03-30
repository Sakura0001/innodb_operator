-- UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0, `varchar_col` = CONCAT('mi_', COALESCE(`varchar_col`, '')) WHERE `varchar_col` IS NOT NULL;
-- 测试逆序索引 varchar_col DESC 下同时 UPDATE 索引列与 int_col 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD INDEX `idx_upd_desc_vc` (`varchar_col` DESC);
-- @PREPARE_END

-- @TIMER_START
UPDATE `{{TEST_TABLE_NAME}}` SET `int_col` = 0, `varchar_col` = CONCAT('mi_', COALESCE(`varchar_col`, '')) WHERE `varchar_col` IS NOT NULL;
-- @TIMER_END
