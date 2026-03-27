-- CREATE INDEX `idx_text_set` ON `{{TEST_TABLE_NAME}}` (`text_col`(20), `set_col`);
-- 测试 text 前缀列与 set 列组合建立CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_text_set` ON `{{TEST_TABLE_NAME}}` (`text_col`(20), `set_col`);
-- @TIMER_END
