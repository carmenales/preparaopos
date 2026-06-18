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

$id = isset($_POST['id']) ? (int)$_POST['id'] : 0;

if ($id <= 0) {
    http_response_code(400);
    echo 'Invalid question set id';
    exit;
}

$organismo = nullable_string_from_post('organismo');
$procesoSelectivo = nullable_string_from_post('proceso_selectivo');
$convocatoriaYear = nullable_int_from_post('convocatoria_year');
$turno = nullable_string_from_post('turno');
$tipo = nullable_string_from_post('tipo');
$descripcion = nullable_string_from_post('descripcion');

$sql = "
    UPDATE question_sets
    SET
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
    http_response_code(500);
    echo 'Could not prepare update statement';
    exit;
}

mysqli_stmt_bind_param(
    $stmt,
    "ssisssi",
    $organismo,
    $procesoSelectivo,
    $convocatoriaYear,
    $turno,
    $tipo,
    $descripcion,
    $id
);

if (!mysqli_stmt_execute($stmt)) {
    http_response_code(500);
    echo 'Could not update question set metadata';
    exit;
}

header('Location: ../progreso_cuestionarios.php?updated_question_set=1');
exit;
