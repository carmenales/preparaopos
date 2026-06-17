<?php

require_once __DIR__ . '/../includes/config.php';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$rawBody = file_get_contents('php://input');
$data = json_decode($rawBody, true);

if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid JSON payload']);
    exit;
}

function required_string($data, $key) {
    if (!isset($data[$key])) {
        return '';
    }

    return trim((string)$data[$key]);
}

function nullable_string($data, $key) {
    if (!isset($data[$key]) || $data[$key] === '') {
        return null;
    }

    return trim((string)$data[$key]);
}

function nullable_int($data, $key) {
    if (!isset($data[$key]) || $data[$key] === '' || $data[$key] === null) {
        return null;
    }

    if (!is_numeric($data[$key])) {
        return null;
    }

    return (int)$data[$key];
}

$testSessionId = required_string($data, 'test_session_id');
$questionId = nullable_int($data, 'question_id');
$selectedAnswer = required_string($data, 'selected_answer');
$correctAnswer = required_string($data, 'correct_answer');
$isCorrect = nullable_int($data, 'is_correct');
$categoria = nullable_string($data, 'categoria');
$bloque = nullable_int($data, 'bloque');
$tema = nullable_int($data, 'tema');

if (!preg_match('/^[a-f0-9]{32}$/', $testSessionId)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid test_session_id']);
    exit;
}

if ($questionId === null || $questionId <= 0) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid question_id']);
    exit;
}

if ($isCorrect !== 0 && $isCorrect !== 1) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid is_correct value']);
    exit;
}

$sql = "
    INSERT INTO test_attempts
        (test_session_id, question_id, selected_answer, correct_answer, is_correct, categoria, bloque, tema)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)
";

$stmt = mysqli_prepare($link, $sql);

if ($stmt === false) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Could not prepare insert statement',
        'details' => mysqli_error($link)
    ]);
    exit;
}

mysqli_stmt_bind_param(
    $stmt,
    "sissisii",
    $testSessionId,
    $questionId,
    $selectedAnswer,
    $correctAnswer,
    $isCorrect,
    $categoria,
    $bloque,
    $tema
);

if (!mysqli_stmt_execute($stmt)) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Could not save test attempt',
        'details' => mysqli_stmt_error($stmt)
    ]);
    exit;
}

$attemptId = mysqli_insert_id($link);

echo json_encode([
    'success' => true,
    'attempt_id' => $attemptId
]);
exit;
