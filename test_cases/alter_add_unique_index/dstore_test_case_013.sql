-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_small_medium` (`smallint_col`, `mediumint_col`);
-- 测试 smallint 与 mediumint 列组合建立唯一索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`smallint_col`, `mediumint_col`) VALUES (1, 11), (2, 22);
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_small_medium` (`smallint_col`, `mediumint_col`);
-- @TIMER_END
