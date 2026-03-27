-- CREATE INDEX `idx_time_varchar_visible` ON `{{TEST_TABLE_NAME}}` (`time_col`, `varchar_col`(16)) VISIBLE;
-- 测试 time 与 varchar 前缀列在 VISIBLE 组合下CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_time_varchar_visible` ON `{{TEST_TABLE_NAME}}` (`time_col`, `varchar_col`(16)) VISIBLE;
-- @TIMER_END
