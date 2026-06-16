USE `preparadortai`;

CREATE TABLE IF NOT EXISTS `test_attempts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `selected_answer` varchar(1024) NOT NULL,
  `correct_answer` varchar(1024) NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `categoria` varchar(255) DEFAULT NULL,
  `bloque` tinyint(4) DEFAULT NULL,
  `tema` tinyint(4) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_test_attempts_question_id` (`question_id`),
  KEY `idx_test_attempts_categoria` (`categoria`),
  KEY `idx_test_attempts_bloque_tema` (`bloque`, `tema`),
  KEY `idx_test_attempts_created_at` (`created_at`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;