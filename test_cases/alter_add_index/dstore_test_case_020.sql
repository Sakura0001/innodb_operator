-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD KEY `idx_char_text_prefix` (`char_col`, `text_col`(15));
-- 测试 char 与 text 前缀列组合建立索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD KEY `idx_char_text_prefix` (`char_col`, `text_col`(15));
-- @TIMER_END
