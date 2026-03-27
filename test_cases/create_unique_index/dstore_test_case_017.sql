-- CREATE UNIQUE INDEX `idx_unique_time_varchar` ON `{{TEST_TABLE_NAME}}` (`time_col`, `varchar_col`(16));
-- 测试 time 与 varchar 前缀列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`time_col`, `varchar_col`) VALUES ('09:00:00', 'time_varchar_a'), ('10:00:00', 'time_varchar_b');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_time_varchar` ON `{{TEST_TABLE_NAME}}` (`time_col`, `varchar_col`(16));
-- @TIMER_END
