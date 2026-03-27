-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_ft_inv_old` TO `idx_rename_ft_inv_new`;
-- 测试重命名 INVISIBLE FULLTEXT 索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT INDEX `idx_rename_ft_inv_old` (`varchar_col`, `text_col`) INVISIBLE;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_ft_inv_old` TO `idx_rename_ft_inv_new`;
-- @TIMER_END
