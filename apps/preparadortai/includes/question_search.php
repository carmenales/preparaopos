<?php

function topic_search_safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function topic_search_truncate($value, $length = 180) {
    $value = trim((string)($value ?? ''));

    if (function_exists('mb_strlen') && function_exists('mb_substr')) {
        return mb_strlen($value, 'UTF-8') > $length
            ? mb_substr($value, 0, $length, 'UTF-8') . '...'
            : $value;
    }

    return strlen($value) > $length
        ? substr($value, 0, $length) . '...'
        : $value;
}

function topic_search_normalize_terms($query, $maxTerms = 8) {
    $query = trim((string)$query);

    if ($query === '') {
        return [];
    }

    if (function_exists('mb_substr')) {
        $query = mb_substr($query, 0, 200, 'UTF-8');
    } else {
        $query = substr($query, 0, 200);
    }

    preg_match_all('/"([^"]+)"|(\S+)/u', $query, $matches, PREG_SET_ORDER);

    $terms = [];

    foreach ($matches as $match) {
        $term = trim($match[1] !== '' ? $match[1] : $match[2]);

        if ($term === '') {
            continue;
        }

        $key = function_exists('mb_strtolower')
            ? mb_strtolower($term, 'UTF-8')
            : strtolower($term);

        $terms[$key] = $term;

        if (count($terms) >= $maxTerms) {
            break;
        }
    }

    return array_values($terms);
}

function topic_search_bind_params($stmt, $types, &$params) {
    if ($types === '' || empty($params)) {
        return;
    }

    $refs = [$types];

    foreach ($params as $key => $value) {
        $refs[] = &$params[$key];
    }

    call_user_func_array([$stmt, 'bind_param'], $refs);
}

function topic_search_categories($link) {
    $categories = [];
    $sql = "
        SELECT DISTINCT categoria
        FROM ptype
        WHERE categoria IS NOT NULL AND categoria <> ''
        ORDER BY categoria ASC
    ";

    $result = mysqli_query($link, $sql);

    if (!$result) {
        return [];
    }

    while ($row = mysqli_fetch_assoc($result)) {
        $categories[] = $row['categoria'];
    }

    mysqli_free_result($result);

    return $categories;
}

function topic_search_questions($link, $filters, $limit = 500) {
    $query = trim((string)($filters['q'] ?? ''));
    $category = trim((string)($filters['categoria'] ?? ''));
    $block = trim((string)($filters['bloque'] ?? ''));
    $topic = trim((string)($filters['tema'] ?? ''));
    $terms = topic_search_normalize_terms($query);

    $where = [];
    $having = [];
    $types = '';
    $params = [];

    if ($category !== '') {
        $where[] = 'p.categoria = ?';
        $types .= 's';
        $params[] = $category;
    }

    if ($block !== '') {
        $where[] = 'p.bloque = ?';
        $types .= 'i';
        $params[] = (int)$block;
    }

    if ($topic !== '') {
        $where[] = 'p.tema = ?';
        $types .= 'i';
        $params[] = (int)$topic;
    }

    $searchableText = "CONCAT_WS(' ',
        COALESCE(p.pregunta, ''),
        COALESCE(p.respuesta, ''),
        COALESCE(p.justif, ''),
        COALESCE(p.categoria, ''),
        COALESCE(i.respuesta, ''),
        COALESCE(i.justif, '')
    )";

    foreach ($terms as $term) {
        $having[] = "MAX($searchableText LIKE ?) = 1";
        $types .= 's';
        $params[] = '%' . $term . '%';
    }

    $whereSql = empty($where) ? '' : 'WHERE ' . implode(' AND ', $where);
    $havingSql = empty($having) ? '' : 'HAVING ' . implode(' AND ', $having);
    $limit = max(1, min((int)$limit, 500));

    $sql = "
        SELECT
            p.id,
            p.pregunta,
            p.categoria,
            p.bloque,
            p.tema
        FROM ptype p
        LEFT JOIN incorrectas i
            ON i.id_pregunta = p.id
        $whereSql
        GROUP BY
            p.id,
            p.pregunta,
            p.categoria,
            p.bloque,
            p.tema
        $havingSql
        ORDER BY p.categoria ASC, p.id DESC
        LIMIT $limit
    ";

    $stmt = mysqli_prepare($link, $sql);

    if (!$stmt) {
        throw new RuntimeException('No se ha podido preparar la búsqueda temática.');
    }

    topic_search_bind_params($stmt, $types, $params);

    if (!mysqli_stmt_execute($stmt)) {
        $error = mysqli_stmt_error($stmt);
        mysqli_stmt_close($stmt);
        throw new RuntimeException('No se ha podido ejecutar la búsqueda temática: ' . $error);
    }

    $result = mysqli_stmt_get_result($stmt);
    $rows = [];

    while ($row = mysqli_fetch_assoc($result)) {
        $rows[] = $row;
    }

    mysqli_stmt_close($stmt);

    return $rows;
}
