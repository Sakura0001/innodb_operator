-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_sp_renamed_new`;
-- 测试重命名后的 SPATIAL 索引删除的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD COLUMN `pt_drop_rename` POINT SRID 0 NULL;
UPDATE `{{TEST_TABLE_NAME}}` SET `pt_drop_rename` = ST_GeomFromText('POINT(18 18)');
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `pt_drop_rename` POINT SRID 0 NOT NULL;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_drop_sp_renamed_old` (`pt_drop_rename`);
ALTER TABLE `{{TEST_TABLE_NAME}}` RENAME INDEX `idx_drop_sp_renamed_old` TO `idx_drop_sp_renamed_new`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP INDEX `idx_drop_sp_renamed_new`;
-- @TIMER_END
