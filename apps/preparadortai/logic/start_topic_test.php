<?php
require_once __DIR__ . '/../includes/config.php';
require_once __DIR__ . '/../includes/question_search.php';

function topic_test_redirect_error($message, $queries = []) {
    $params = ['error' => $message];

    if (!empty($queries)) {
        $params['topics'] = $queries;
    }

    header('Location: ../practica_tematica.php?' . http_build_query($params));
    exit;
}

function topic_test_insert_session($link, $sessionId, $queries, $correctionMode, $questionIds) {
    $title = empty($queries)
        ? 'Práctica temática'
        : 'Práctica temática: ' . implode(' + ', $queries);

    if (function_exists('mb_substr')) {
        $title = mb_substr($title, 0, 255, 'UTF-8');
    } else {
        $title = substr($title, 0, 255);
    }

    $totalQuestions = count($questionIds);

    $sql = "
        INSERT INTO test_sessions
            (id, mode, title, correction_mode, total_questions)
        VALUES
            (?, 'tematico', ?, ?, ?)
    ";

    $stmt = mysqli_prepare($link, $sql);

    if (!$stmt) {
        throw new RuntimeException('No se ha podido preparar el registro de la sesión.');
    }

    mysqli_stmt_bind_param($stmt, 'sssi', $sessionId, $title, $correctionMode, $totalQuestions);

    if (!mysqli_stmt_execute($stmt)) {
        $error = mysqli_stmt_error($stmt);
        mysqli_stmt_close($stmt);
        throw new RuntimeException('No se ha podido registrar la sesión: ' . $error);
    }

    mysqli_stmt_close($stmt);

    foreach ($queries as $position => $query) {
        $topicSql = "
            INSERT INTO test_session_topics
                (test_session_id, topic_label, position)
            VALUES
                (?, ?, ?)
        ";
        $topicStmt = mysqli_prepare($link, $topicSql);

        if (!$topicStmt) {
            throw new RuntimeException('No se ha podido preparar el registro de una temática.');
        }

        mysqli_stmt_bind_param($topicStmt, 'ssi', $sessionId, $query, $position);

        if (!mysqli_stmt_execute($topicStmt)) {
            $error = mysqli_stmt_error($topicStmt);
            mysqli_stmt_close($topicStmt);
            throw new RuntimeException('No se ha podido registrar una temática: ' . $error);
        }

        $topicId = mysqli_insert_id($link);
        mysqli_stmt_close($topicStmt);

        $matchingRows = topic_search_questions($link, ['topics' => [$query]], 500);
        $matchingIds = [];

        foreach ($matchingRows as $row) {
            $matchingIds[(int)$row['id']] = true;
        }

        $mapSql = "
            INSERT IGNORE INTO test_session_question_topics
                (test_session_id, question_id, topic_id)
            VALUES
                (?, ?, ?)
        ";
        $mapStmt = mysqli_prepare($link, $mapSql);

        if (!$mapStmt) {
            throw new RuntimeException('No se ha podido preparar la relación entre temática y pregunta.');
        }

        foreach ($questionIds as $questionId) {
            if (!isset($matchingIds[(int)$questionId])) {
                continue;
            }

            mysqli_stmt_bind_param($mapStmt, 'sii', $sessionId, $questionId, $topicId);

            if (!mysqli_stmt_execute($mapStmt)) {
                $error = mysqli_stmt_error($mapStmt);
                mysqli_stmt_close($mapStmt);
                throw new RuntimeException('No se ha podido relacionar una pregunta con su temática: ' . $error);
            }
        }

        mysqli_stmt_close($mapStmt);
    }
}

$topics = $_POST['topics'] ?? [];

if (empty($topics) && !empty($_GET['topics'])) {
    $topics = is_array($_GET['topics']) ? $_GET['topics'] : [$_GET['topics']];
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST' && empty($topics)) {
    topic_test_redirect_error('Solicitud no válida.');
}

$queries = topic_search_normalize_queries($topics, $_POST['q'] ?? '');
$correctionMode = ($_POST['correccion'] ?? '') === 'final' ? 'final' : 'inmediata';
$rawIds = $_POST['question_ids'] ?? [];

if (!is_array($rawIds)) {
    topic_test_redirect_error('La selección de preguntas no es válida.', $queries);
}

$ids = [];

foreach ($rawIds as $rawId) {
    $value = filter_var($rawId, FILTER_VALIDATE_INT, [
        'options' => ['min_range' => 1],
    ]);

    if ($value !== false) {
        $ids[(int)$value] = (int)$value;
    }
}

$ids = array_values($ids);

if (empty($ids)) {
    topic_test_redirect_error('Selecciona al menos una pregunta.', $queries);
}

if (count($ids) > 500) {
    topic_test_redirect_error('La selección supera el máximo permitido.', $queries);
}

$idSql = implode(',', array_map('intval', $ids));
$result = mysqli_query($link, "SELECT id FROM ptype WHERE id IN ($idSql)");
$existing = [];

if ($result) {
    while ($row = mysqli_fetch_assoc($result)) {
        $existing[(int)$row['id']] = (int)$row['id'];
    }
    mysqli_free_result($result);
}

$ids = array_values(array_intersect($ids, array_values($existing)));

if (empty($ids)) {
    topic_test_redirect_error('Las preguntas seleccionadas ya no están disponibles.', $queries);
}

$maxQuestions = filter_var($_POST['max_questions'] ?? count($ids), FILTER_VALIDATE_INT, [
    'options' => [
        'default' => count($ids),
        'min_range' => 1,
        'max_range' => 100,
    ],
]);

$maxQuestions = min((int)$maxQuestions, count($ids), 100);
shuffle($ids);
$ids = array_slice($ids, 0, $maxQuestions);
$testSessionId = bin2hex(random_bytes(16));

mysqli_begin_transaction($link);

try {
    topic_test_insert_session(
        $link,
        $testSessionId,
        $queries,
        $correctionMode,
        $ids
    );
    mysqli_commit($link);
} catch (Throwable $exception) {
    mysqli_rollback($link);
    topic_test_redirect_error($exception->getMessage(), $queries);
}

$params = [
    'modo' => 'tematico',
    'ids' => implode(',', $ids),
    'test_session_id' => $testSessionId,
];

if (!empty($queries)) {
    $params['topics'] = $queries;
}

if ($correctionMode === 'final') {
    $params['correccion'] = 'final';
}

header('Location: ../test.php?' . http_build_query($params));
exit;
