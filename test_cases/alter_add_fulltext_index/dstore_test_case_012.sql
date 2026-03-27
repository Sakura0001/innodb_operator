-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT INDEX `idx_ft_text_medium_long` (`text_col`, `mediumtext_col`, `longtext_col`);
-- 测试 text、mediumtext、longtext 多列 FULLTEXT 索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD FULLTEXT INDEX `idx_ft_text_medium_long` (`text_col`, `mediumtext_col`, `longtext_col`);
-- @TIMER_END
