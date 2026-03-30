-- ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `mediumint_col` mediumint unsigned NULL;
-- 测试将 mediumint_col 修改为 NULL 的执行情况

-- @PREPARE_START
DROP TABLE IF EXISTS `{{TEST_TABLE_NAME}}`;
CREATE TABLE `{{TEST_TABLE_NAME}}` LIKE `{{BASE_TABLE_NAME}}`;
INSERT INTO `{{TEST_TABLE_NAME}}` SELECT * FROM `{{BASE_TABLE_NAME}}`;
UPDATE `{{TEST_TABLE_NAME}}` SET `mediumint_col` = 1 WHERE `mediumint_col` IS NULL;
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `mediumint_col` mediumint unsigned NOT NULL;
-- @PREPARE_END

-- @TIMER_START
ALTER TABLE `{{TEST_TABLE_NAME}}` MODIFY COLUMN `mediumint_col` mediumint unsigned NULL;
-- @TIMER_END
