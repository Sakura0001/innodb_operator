-- ALTER TABLE `{{TEST_TABLE_NAME}}` DROP COLUMN `id_col`;
-- 测试删除单列表唯一剩余列时报错的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
ALTER TABLE `{{TEST_TABLE_NAME}}`
  DROP COLUMN `int_col`,
  DROP COLUMN `bigint_col`,
  DROP COLUMN `year_col`,
  DROP COLUMN `char_col`,
  DROP COLUMN `tinyint_col`,
  DROP COLUMN `bool_col`,
  DROP COLUMN `smallint_col`,
  DROP COLUMN `mediumint_col`,
  DROP COLUMN `decimal_col`,
  DROP COLUMN `float_col`,
  DROP COLUMN `double_col`,
  DROP COLUMN `date_col`,
  DROP COLUMN `datetime_col`,
  DROP COLUMN `timestamp_col`,
  DROP COLUMN `time_col`,
  DROP COLUMN `varchar_col`,
  DROP COLUMN `binary_col`,
  DROP COLUMN `varbinary_col`,
  DROP COLUMN `tinyblob_col`,
  DROP COLUMN `blob_col`,
  DROP COLUMN `mediumblob_col`,
  DROP COLUMN `longblob_col`,
  DROP COLUMN `tinytext_col`,
  DROP COLUMN `text_col`,
  DROP COLUMN `mediumtext_col`,
  DROP COLUMN `longtext_col`,
  DROP COLUMN `enum_col`,
  DROP COLUMN `set_col`,
  DROP COLUMN `bit_col`,
  DROP COLUMN `unsigned_int_col`,
  DROP COLUMN `unsigned_decimal_col`;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` DROP COLUMN `id_col`;
-- @TIMER_END
