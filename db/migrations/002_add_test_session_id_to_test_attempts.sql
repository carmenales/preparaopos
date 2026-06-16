USE `preparadortai`;

ALTER TABLE `test_attempts`
  ADD COLUMN `test_session_id` varchar(64) DEFAULT NULL AFTER `id`,
  ADD KEY `idx_test_attempts_session_id` (`test_session_id`);