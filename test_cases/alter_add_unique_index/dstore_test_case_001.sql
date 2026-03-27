-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD CONSTRAINT `uq_varchar_enum` UNIQUE INDEX `idx_unique_varchar_enum` USING BTREE (`varchar_col`(32), `enum_col` DESC) COMMENT 'uq_varchar_enum' VISIBLE;
-- 测试 varchar 前缀列与 enum 列在命名、COMMENT、VISIBLE 组合下建立唯一索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`varchar_col`, `enum_col`) VALUES ('uqve_a', 'aaa'), ('uqve_b', 'bbb');
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD CONSTRAINT `uq_varchar_enum` UNIQUE INDEX `idx_unique_varchar_enum` USING BTREE (`varchar_col`(32), `enum_col` DESC) COMMENT 'uq_varchar_enum' VISIBLE;
-- @TIMER_END
