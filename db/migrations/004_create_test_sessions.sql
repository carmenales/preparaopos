-- Metadatos de sesiones y trazabilidad de prácticas temáticas.
-- Compatible con MariaDB 10.5+.

CREATE TABLE IF NOT EXISTS test_sessions (
    id CHAR(32) NOT NULL,
    mode VARCHAR(30) NOT NULL DEFAULT 'standard',
    title VARCHAR(255) NULL,
    correction_mode VARCHAR(20) NOT NULL DEFAULT 'inmediata',
    total_questions SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_test_sessions_mode_created (mode, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS test_session_topics (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    test_session_id CHAR(32) NOT NULL,
    topic_label VARCHAR(200) NOT NULL,
    position SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE KEY uq_test_session_topic_position (test_session_id, position),
    KEY idx_test_session_topics_label (topic_label),
    CONSTRAINT fk_test_session_topics_session
        FOREIGN KEY (test_session_id)
        REFERENCES test_sessions (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS test_session_question_topics (
    test_session_id CHAR(32) NOT NULL,
    question_id INT NOT NULL,
    topic_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (test_session_id, question_id, topic_id),
    KEY idx_tsqt_topic_question (topic_id, question_id),
    KEY idx_tsqt_question (question_id),
    CONSTRAINT fk_tsqt_session
        FOREIGN KEY (test_session_id)
        REFERENCES test_sessions (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_tsqt_topic
        FOREIGN KEY (topic_id)
        REFERENCES test_session_topics (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
