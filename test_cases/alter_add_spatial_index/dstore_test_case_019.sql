-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_multipoint_dup` (`multipoint_dup_col`);
-- 测试重复 MULTIPOINT 空间索引名时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD COLUMN `multipoint_dup_col` MULTIPOINT SRID 0 NULL;
UPDATE `{{TEST_TABLE_NAME}}` SET `multipoint_dup_col` = ST_GeomFromText('MULTIPOINT((3 3),(4 4))');
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `multipoint_dup_col` MULTIPOINT SRID 0 NOT NULL;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_multipoint_dup` (`multipoint_dup_col`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_multipoint_dup` (`multipoint_dup_col`);
-- @TIMER_END
