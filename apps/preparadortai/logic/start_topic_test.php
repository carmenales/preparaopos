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

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    topic_test_redirect_error('Solicitud no válida.');
}

$queries = topic_search_normalize_queries($_POST['topics'] ?? [], $_POST['q'] ?? '');
$correction = ($_POST['correccion'] ?? '') === 'final' ? 'final' : 'inmediata';
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

$params = [
    'modo' => 'tematico',
    'ids' => implode(',', $ids),
];

if (!empty($queries)) {
    $params['topics'] = $queries;
}

if ($correction === 'final') {
    $params['correccion'] = 'final';
}

header('Location: ../test.php?' . http_build_query($params));
exit;
