<?php

require_once __DIR__ . '/../includes/config.php';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true);

if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Invalid JSON payload']);
    exit;
}

$testSessionId = isset($data['test_session_id']) ? trim($data['test_session_id']) : null;
$questionId = isset($data['question_id']) ? (int) $data['question_id'] : 0;
$selectedAnswer = isset($data['selected_answer']) ? trim($data['selected_answer']) : '';
$correctAnswer = isset($data['correct_answer']) ? trim($data['correct_answer']) : '';
$isCorrect = !empty($data['is_correct']) ? 1 : 0;
$categoria = isset($data['categoria']) ? trim($data['categoria']) : null;
$bloque = isset($data['bloque']) && $data['bloque'] !== '' ? (int) $data['bloque'] : null;
$tema = isset($data['tema']) && $data['tema'] !== '' ? (int) $data['tema'] : null;

if ($questionId <= 0 || $selectedAnswer === '' || $correctAnswer === '') {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Missing required attempt data']);
    exit;
}

$sql = "INSERT INTO test_attempts
    (test_session_id, question_id, selected_answer, correct_answer, is_correct, categoria, bloque, tema)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)";

$stmt = mysqli_prepare($link, $sql);

if ($stmt === false) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Could not prepare statement']);
    exit;
}

mysqli_stmt_bind_param(
    $stmt,
    "issisii",
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
    echo json_encode(['success' => false, 'message' => 'Could not save attempt']);
    exit;
}

echo json_encode([
    'success' => true,
    'attempt_id' => mysqli_insert_id($link)
]);