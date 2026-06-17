<?php

require_once __DIR__ . '/../includes/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'Method not allowed';
    exit;
}

$testSessionId = isset($_POST['test_session_id']) ? trim($_POST['test_session_id']) : '';

if (!preg_match('/^[a-f0-9]{32}$/', $testSessionId)) {
    http_response_code(400);
    echo 'Invalid test session id';
    exit;
}

$sql = "DELETE FROM test_attempts WHERE test_session_id = ?";
$stmt = mysqli_prepare($link, $sql);

if ($stmt === false) {
    http_response_code(500);
    echo 'Could not prepare delete statement';
    exit;
}

mysqli_stmt_bind_param($stmt, "s", $testSessionId);

if (!mysqli_stmt_execute($stmt)) {
    http_response_code(500);
    echo 'Could not delete test session attempts';
    exit;
}

$deletedRows = mysqli_stmt_affected_rows($stmt);

header('Location: ../estadisticas.php?deleted_attempts=' . $deletedRows);
exit;
