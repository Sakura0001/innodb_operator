-- CREATE INDEX `idx_char_text_prefix` ON `{{TEST_TABLE_NAME}}` (`char_col`, `text_col`(15));
-- 测试 char 与 text 前缀列组合CREATE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
CREATE INDEX `idx_char_text_prefix` ON `{{TEST_TABLE_NAME}}` (`char_col`, `text_col`(15));
-- @TIMER_END
