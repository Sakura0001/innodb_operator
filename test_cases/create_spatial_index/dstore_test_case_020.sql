-- CREATE SPATIAL INDEX `idx_sp_geom_nullable` ON `{{TEST_TABLE_NAME}}` (`geometry_nullable_col`);
-- 测试可空 GEOMETRY 列执行 CREATE SPATIAL INDEX 时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD COLUMN `geometry_nullable_col` GEOMETRY SRID 0 NULL;
UPDATE `{{TEST_TABLE_NAME}}` SET `geometry_nullable_col` = ST_GeomFromText('POINT(23 23)');
-- @PREPARE_END

-- @TIMER_START
CREATE SPATIAL INDEX `idx_sp_geom_nullable` ON `{{TEST_TABLE_NAME}}` (`geometry_nullable_col`);
-- @TIMER_END
