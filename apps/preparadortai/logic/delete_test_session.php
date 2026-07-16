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

mysqli_begin_transaction($link);

try {
    $stmt = mysqli_prepare($link, 'DELETE FROM test_attempts WHERE test_session_id = ?');

    if (!$stmt) {
        throw new RuntimeException('Could not prepare attempts delete statement');
    }

    mysqli_stmt_bind_param($stmt, 's', $testSessionId);

    if (!mysqli_stmt_execute($stmt)) {
        throw new RuntimeException('Could not delete test session attempts');
    }

    $deletedRows = mysqli_stmt_affected_rows($stmt);
    mysqli_stmt_close($stmt);

    $sessionStmt = mysqli_prepare($link, 'DELETE FROM test_sessions WHERE id = ?');

    if (!$sessionStmt) {
        throw new RuntimeException('Could not prepare session metadata delete statement');
    }

    mysqli_stmt_bind_param($sessionStmt, 's', $testSessionId);

    if (!mysqli_stmt_execute($sessionStmt)) {
        throw new RuntimeException('Could not delete test session metadata');
    }

    mysqli_stmt_close($sessionStmt);
    mysqli_commit($link);
} catch (Throwable $exception) {
    mysqli_rollback($link);
    http_response_code(500);
    echo $exception->getMessage();
    exit;
}

header('Location: ../estadisticas.php?deleted_attempts=' . $deletedRows);
exit;
