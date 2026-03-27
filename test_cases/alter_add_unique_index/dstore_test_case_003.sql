-- ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_unsigned_date` (`unsigned_int_col`, `date_col`) INVISIBLE;
-- 测试 unsigned int 与 date 列在 INVISIBLE 组合下建立唯一索引的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
DELETE FROM `{{TEST_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` (`unsigned_int_col`, `date_col`) VALUES (11, '2024-02-01'), (22, '2024-02-02');
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` ADD UNIQUE INDEX `idx_unique_unsigned_date` (`unsigned_int_col`, `date_col`) INVISIBLE;
-- @TIMER_END
