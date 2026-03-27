-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_dup_implicit` (`pt_dup_implicit`);
-- 测试隐式空间索引命中重复索引名时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD COLUMN `pt_dup_implicit` POINT SRID 0 NULL;
UPDATE `{{TEST_TABLE_NAME}}` SET `pt_dup_implicit` = ST_GeomFromText('POINT(16 16)');
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `pt_dup_implicit` POINT SRID 0 NOT NULL;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_dup_implicit` (`pt_dup_implicit`);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_dup_implicit` (`pt_dup_implicit`);
-- @TIMER_END
