-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_ft_created_old` TO `idx_rename_ft_created_new`;
-- 测试重命名由 CREATE FULLTEXT INDEX 创建的索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
CREATE FULLTEXT INDEX `idx_rename_ft_created_old` ON `{{TEST_TABLE_NAME}}` (`varchar_col`, `text_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_rename_ft_created_old` TO `idx_rename_ft_created_new`;
-- @TIMER_END
