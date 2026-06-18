CREATE TABLE IF NOT EXISTS question_sets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(255) NOT NULL UNIQUE,
    organismo VARCHAR(100) NULL,
    proceso_selectivo VARCHAR(150) NULL,
    convocatoria_year INT NULL,
    turno VARCHAR(50) NULL,
    tipo VARCHAR(100) NULL,
    descripcion VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO question_sets (
    categoria,
    organismo,
    proceso_selectivo,
    convocatoria_year,
    turno,
    tipo,
    descripcion
)
SELECT
    source_categories.categoria,
    CASE
        WHEN source_categories.categoria LIKE 'CUESTIONARIO%' THEN 'AGE'
        ELSE NULL
    END AS organismo,
    CASE
        WHEN source_categories.categoria LIKE 'CUESTIONARIO%' THEN 'TAI'
        ELSE NULL
    END AS proceso_selectivo,
    CASE
        WHEN source_categories.categoria LIKE 'CUESTIONARIO 14/%' THEN 2014
        WHEN source_categories.categoria LIKE 'CUESTIONARIO 15/%' THEN 2015
        WHEN source_categories.categoria LIKE 'CUESTIONARIO 16/%' THEN 2016
        WHEN source_categories.categoria LIKE 'CUESTIONARIO 17/%' THEN 2017
        WHEN source_categories.categoria LIKE 'CUESTIONARIO 18/%' THEN 2018
        WHEN source_categories.categoria LIKE 'CUESTIONARIO 19/%' THEN 2019
        WHEN source_categories.categoria LIKE '%2022%' THEN 2022
        WHEN source_categories.categoria LIKE '%2024%' THEN 2024
        ELSE NULL
    END AS convocatoria_year,
    CASE
        WHEN source_categories.categoria LIKE '%TAI–LI%' OR source_categories.categoria LIKE '%TAI-LI%' THEN 'Libre'
        WHEN source_categories.categoria LIKE '%TAI–PI%' OR source_categories.categoria LIKE '%TAI-PI%' OR source_categories.categoria LIKE '%TAI PI%' THEN 'Promocion interna'
        ELSE NULL
    END AS turno,
    CASE
        WHEN source_categories.categoria LIKE 'CUESTIONARIO%' THEN 'Examen oficial'
        ELSE 'Test tematico'
    END AS tipo,
    NULL AS descripcion
FROM (
    SELECT DISTINCT categoria
    FROM ptype
    WHERE categoria IS NOT NULL AND categoria <> ''
) source_categories
ON DUPLICATE KEY UPDATE
    categoria = VALUES(categoria);
