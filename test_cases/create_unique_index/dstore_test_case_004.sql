-- CREATE UNIQUE INDEX `idx_unique_char_set` ON `{{TEST_TABLE_NAME}}` (`char_col`, `set_col`);
-- 测试 char 与 set 列组合CREATE UNIQUE INDEX的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`char_col`, `set_col`) VALUES ('c001', '111'), ('c002', '222');
-- @PREPARE_END

-- @TIMER_START
CREATE UNIQUE INDEX `idx_unique_char_set` ON `{{TEST_TABLE_NAME}}` (`char_col`, `set_col`);
-- @TIMER_END
