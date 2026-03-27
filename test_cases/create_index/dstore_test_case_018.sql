-- CREATE INDEX `idx_medium_longtext` ON `{{TEST_TABLE_NAME}}` (`mediumtext_col`(40), `longtext_col`(60));
-- 测试 mediumtext 与 longtext 前缀列组合CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_medium_longtext` ON `{{TEST_TABLE_NAME}}` (`mediumtext_col`(40), `longtext_col`(60));
-- @TIMER_END
