-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_polygon_point_multi` (`polygon_multi_col`, `point_multi_col`);
-- 测试 SPATIAL 索引作用于 polygon 与 point 多列组合时的报错记录

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD COLUMN `polygon_multi_col` POLYGON SRID 0 NULL, ADD COLUMN `point_multi_col` POINT SRID 0 NULL;
UPDATE `{{TEST_TABLE_NAME}}` SET `polygon_multi_col` = ST_GeomFromText('POLYGON((0 0,0 2,2 2,2 0,0 0))'), `point_multi_col` = ST_GeomFromText('POINT(15 15)');
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `polygon_multi_col` POLYGON SRID 0 NOT NULL, MODIFY COLUMN `point_multi_col` POINT SRID 0 NOT NULL;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD SPATIAL INDEX `idx_sp_polygon_point_multi` (`polygon_multi_col`, `point_multi_col`);
-- @TIMER_END
