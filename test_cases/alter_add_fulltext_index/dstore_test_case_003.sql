-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT KEY `idx_ft_parser` (`tinytext_col`, `mediumtext_col`) WITH PARSER ngram;
-- 测试 tinytext 与 mediumtext 列在 WITH PARSER ngram 组合下建立 FULLTEXT 索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT KEY `idx_ft_parser` (`tinytext_col`, `mediumtext_col`) WITH PARSER ngram;
-- @TIMER_END
