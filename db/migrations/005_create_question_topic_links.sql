USE `preparadortai`;

-- Hasta ahora `question_sets` (una fila por `categoria`) no sabía a qué
-- proceso selectivo pertenece más allá de organismo/proceso_selectivo/año,
-- que son texto libre sin relación con las carpetas de knowledge/.
-- `proceso_slug` usa el mismo slug que la ruta bajo knowledge/processes/
-- (ej. "comunidad-madrid/administracion-digital/ia"), para poder cruzar
-- ambos sistemas por el mismo identificador el día que haga falta.
ALTER TABLE `question_sets`
  ADD COLUMN `proceso_slug` VARCHAR(150) DEFAULT NULL AFTER `proceso_selectivo`;

-- Enlace entre una pregunta (identificada por categoria + bloque + tema,
-- la numeración interna que ya existe en test_attempts/ptype) y un apunte
-- de knowledge/ (identificado por su `id` de frontmatter, ej.
-- "cm-ad-ia-tema-001-fundamentos-inteligencia-artificial").
--
-- No hay FOREIGN KEY hacia knowledge_note_id porque los apuntes viven en
-- ficheros Markdown, no en esta base de datos — la integridad referencial
-- de ese lado la garantiza quien cargue los enlaces (a mano o por script),
-- no MySQL.
--
-- Se admite bloque/tema NULL para poder enlazar a nivel de categoria
-- completa cuando todavía no haya numeración fina, y para poder enlazar
-- varios apuntes a un mismo (categoria, bloque, tema) si un tema de examen
-- se corresponde con más de un apunte.
CREATE TABLE IF NOT EXISTS `question_topic_links` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `categoria` VARCHAR(255) NOT NULL,
  `bloque` TINYINT(4) DEFAULT NULL,
  `tema` TINYINT(4) DEFAULT NULL,
  `knowledge_note_id` VARCHAR(150) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_question_topic_link` (`categoria`, `bloque`, `tema`, `knowledge_note_id`),
  KEY `idx_qtl_categoria_bloque_tema` (`categoria`, `bloque`, `tema`),
  KEY `idx_qtl_knowledge_note_id` (`knowledge_note_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
