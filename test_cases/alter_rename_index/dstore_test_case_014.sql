-- ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_sp_created_old` TO `idx_rename_sp_created_new`;
-- 测试重命名由 CREATE SPATIAL INDEX 创建的索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD COLUMN `pt_rename_created` POINT SRID 0 NULL;
UPDATE `{{TEST_TABLE_NAME}}` SET `pt_rename_created` = ST_GeomFromText('POINT(20 20)');
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `pt_rename_created` POINT SRID 0 NOT NULL;
CREATE SPATIAL INDEX `idx_rename_sp_created_old` ON `{{TEST_TABLE_NAME}}` (`pt_rename_created`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME KEY `idx_rename_sp_created_old` TO `idx_rename_sp_created_new`;
-- @TIMER_END
