<?php

/**
 * Consultas sobre question_topic_links (ver
 * db/migrations/005_create_question_topic_links.sql).
 *
 * Deliberadamente sin UI todavía: hoy no hay preguntas del proceso IA
 * Madrid Digital ni apuntes de GSI A2/Auxiliar TIC, así que no hay nada
 * real que enlazar. Estas funciones son la base para cuando sí lo haya,
 * y para un script/página de curación posterior.
 */

/**
 * Ids de apuntes de knowledge/ enlazados a una pregunta concreta,
 * identificada por su categoria + bloque + tema numéricos.
 *
 * @return string[] lista de knowledge_note_id (frontmatter `id` del apunte)
 */
function topic_links_notes_for_question($link, string $categoria, ?int $bloque, ?int $tema): array
{
    $sql = "
        SELECT knowledge_note_id
        FROM question_topic_links
        WHERE categoria = ?
          AND (bloque <=> ?)
          AND (tema <=> ?)
        ORDER BY knowledge_note_id
    ";

    $stmt = mysqli_prepare($link, $sql);
    if (!$stmt) {
        return [];
    }

    mysqli_stmt_bind_param($stmt, 'sii', $categoria, $bloque, $tema);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    $noteIds = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $noteIds[] = $row['knowledge_note_id'];
    }

    return $noteIds;
}

/**
 * Enlaces (categoria, bloque, tema) de pregunta asociados a un apunte
 * concreto de knowledge/, identificado por su knowledge_note_id.
 *
 * @return array<int, array{categoria: string, bloque: ?int, tema: ?int}>
 */
function topic_links_questions_for_note($link, string $knowledgeNoteId): array
{
    $sql = "
        SELECT categoria, bloque, tema
        FROM question_topic_links
        WHERE knowledge_note_id = ?
        ORDER BY categoria, bloque, tema
    ";

    $stmt = mysqli_prepare($link, $sql);
    if (!$stmt) {
        return [];
    }

    mysqli_stmt_bind_param($stmt, 's', $knowledgeNoteId);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    $links = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $links[] = [
            'categoria' => $row['categoria'],
            'bloque' => $row['bloque'] !== null ? (int) $row['bloque'] : null,
            'tema' => $row['tema'] !== null ? (int) $row['tema'] : null,
        ];
    }

    return $links;
}

/**
 * Crea (o ignora si ya existe) un enlace entre una pregunta y un apunte.
 * Pensado para un futuro script/página de curación, no para uso masivo.
 */
function topic_links_create($link, string $categoria, ?int $bloque, ?int $tema, string $knowledgeNoteId): bool
{
    $sql = "
        INSERT IGNORE INTO question_topic_links (categoria, bloque, tema, knowledge_note_id)
        VALUES (?, ?, ?, ?)
    ";

    $stmt = mysqli_prepare($link, $sql);
    if (!$stmt) {
        return false;
    }

    mysqli_stmt_bind_param($stmt, 'siis', $categoria, $bloque, $tema, $knowledgeNoteId);

    return mysqli_stmt_execute($stmt);
}
