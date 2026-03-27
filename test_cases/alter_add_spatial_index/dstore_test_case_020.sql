-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_geom_nullable` (`geometry_nullable_col`);
-- 测试可空 GEOMETRY 列建立 SPATIAL 索引时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD COLUMN `geometry_nullable_col` GEOMETRY SRID 0 NULL;
UPDATE `{{TEST_TABLE_NAME}}` SET `geometry_nullable_col` = ST_GeomFromText('POINT(23 23)');
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_geom_nullable` (`geometry_nullable_col`);
-- @TIMER_END
