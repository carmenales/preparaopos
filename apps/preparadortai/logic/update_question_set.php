<?php

require_once __DIR__ . '/../includes/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'Method not allowed';
    exit;
}

function nullable_string_from_post($key) {
    if (!isset($_POST[$key])) {
        return null;
    }

    $value = trim((string)$_POST[$key]);

    return $value === '' ? null : $value;
}

function nullable_int_from_post($key) {
    if (!isset($_POST[$key])) {
        return null;
    }

    $value = trim((string)$_POST[$key]);

    if ($value === '') {
        return null;
    }

    if (!ctype_digit($value)) {
        return null;
    }

    return (int)$value;
}

function table_exists($link, $tableName) {
    $escapedTable = mysqli_real_escape_string($link, $tableName);
    $result = mysqli_query($link, "SHOW TABLES LIKE '$escapedTable'");

    return $result && mysqli_num_rows($result) > 0;
}

function category_exists_in_table($link, $tableName, $category, $currentCategory) {
    if (!table_exists($link, $tableName)) {
        return false;
    }

    $sql = "SELECT 1 FROM $tableName WHERE categoria = ? AND categoria <> ? LIMIT 1";
    $stmt = mysqli_prepare($link, $sql);

    if ($stmt === false) {
        throw new RuntimeException("Could not prepare duplicate check for $tableName");
    }

    mysqli_stmt_bind_param($stmt, "ss", $category, $currentCategory);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    $exists = mysqli_fetch_assoc($result) !== null;
    mysqli_stmt_close($stmt);

    return $exists;
}

function update_category_in_table($link, $tableName, $oldCategory, $newCategory) {
    if (!table_exists($link, $tableName)) {
        return;
    }

    $sql = "UPDATE $tableName SET categoria = ? WHERE categoria = ?";
    $stmt = mysqli_prepare($link, $sql);

    if ($stmt === false) {
        throw new RuntimeException("Could not prepare category update for $tableName");
    }

    mysqli_stmt_bind_param($stmt, "ss", $newCategory, $oldCategory);

    if (!mysqli_stmt_execute($stmt)) {
        throw new RuntimeException("Could not update category in $tableName");
    }

    mysqli_stmt_close($stmt);
}

$id = isset($_POST['id']) ? (int)$_POST['id'] : 0;

if ($id <= 0) {
    http_response_code(400);
    echo 'Invalid question set id';
    exit;
}

$newCategory = nullable_string_from_post('categoria');
$oldCategory = nullable_string_from_post('old_categoria');

if ($newCategory === null) {
    http_response_code(400);
    echo 'Category cannot be empty';
    exit;
}

$organismo = nullable_string_from_post('organismo');
$procesoSelectivo = nullable_string_from_post('proceso_selectivo');
$convocatoriaYear = nullable_int_from_post('convocatoria_year');
$turno = nullable_string_from_post('turno');
$tipo = nullable_string_from_post('tipo');
$descripcion = nullable_string_from_post('descripcion');

$currentSql = "
    SELECT categoria
    FROM question_sets
    WHERE id = ?
";

$stmt = mysqli_prepare($link, $currentSql);

if ($stmt === false) {
    http_response_code(500);
    echo 'Could not prepare current question set query';
    exit;
}

mysqli_stmt_bind_param($stmt, "i", $id);
mysqli_stmt_execute($stmt);
$currentResult = mysqli_stmt_get_result($stmt);
$currentQuestionSet = mysqli_fetch_assoc($currentResult);
mysqli_stmt_close($stmt);

if (!$currentQuestionSet) {
    http_response_code(404);
    echo 'Question set not found';
    exit;
}

$currentCategory = (string)$currentQuestionSet['categoria'];

if ($oldCategory !== null && $oldCategory !== $currentCategory) {
    http_response_code(409);
    echo 'The category was modified by another operation. Reload the form and try again.';
    exit;
}

$categoryChanged = $newCategory !== $currentCategory;

if ($categoryChanged) {
    $duplicateQuestionSetSql = "
        SELECT id
        FROM question_sets
        WHERE categoria = ?
          AND id <> ?
        LIMIT 1
    ";

    $stmt = mysqli_prepare($link, $duplicateQuestionSetSql);
    mysqli_stmt_bind_param($stmt, "si", $newCategory, $id);
    mysqli_stmt_execute($stmt);
    $duplicateQuestionSetResult = mysqli_stmt_get_result($stmt);
    $duplicateQuestionSet = mysqli_fetch_assoc($duplicateQuestionSetResult);
    mysqli_stmt_close($stmt);

    if ($duplicateQuestionSet) {
        http_response_code(409);
        echo 'A question set with that category already exists';
        exit;
    }

    try {
        if (category_exists_in_table($link, 'ptype', $newCategory, $currentCategory)) {
            http_response_code(409);
            echo 'There are already ptype questions using that category';
            exit;
        }

        if (category_exists_in_table($link, 'rtype', $newCategory, $currentCategory)) {
            http_response_code(409);
            echo 'There are already rtype questions using that category';
            exit;
        }
    } catch (Throwable $exception) {
        http_response_code(500);
        echo $exception->getMessage();
        exit;
    }
}

mysqli_begin_transaction($link);

try {
    $sql = "
        UPDATE question_sets
        SET
            categoria = ?,
            organismo = ?,
            proceso_selectivo = ?,
            convocatoria_year = ?,
            turno = ?,
            tipo = ?,
            descripcion = ?
        WHERE id = ?
    ";

    $stmt = mysqli_prepare($link, $sql);

    if ($stmt === false) {
        throw new RuntimeException('Could not prepare update statement');
    }

    mysqli_stmt_bind_param(
        $stmt,
        "sssisssi",
        $newCategory,
        $organismo,
        $procesoSelectivo,
        $convocatoriaYear,
        $turno,
        $tipo,
        $descripcion,
        $id
    );

    if (!mysqli_stmt_execute($stmt)) {
        throw new RuntimeException('Could not update question set metadata');
    }

    mysqli_stmt_close($stmt);

    if ($categoryChanged) {
        update_category_in_table($link, 'ptype', $currentCategory, $newCategory);
        update_category_in_table($link, 'rtype', $currentCategory, $newCategory);
        update_category_in_table($link, 'test_attempts', $currentCategory, $newCategory);
    }

    mysqli_commit($link);
} catch (Throwable $exception) {
    mysqli_rollback($link);
    http_response_code(500);
    echo $exception->getMessage();
    exit;
}

header('Location: ../categorias.php?updated_question_set=1');
exit;
