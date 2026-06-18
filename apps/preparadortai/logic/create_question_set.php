<?php

require_once __DIR__ . '/../includes/config.php';

function clean_value($value) {
    $value = trim((string)($value ?? ''));
    return $value === '' ? null : $value;
}

function redirect_with_error($error, $categoria = '') {
    $url = '../nueva_categoria.php?error=' . urlencode($error);

    if ($categoria !== '') {
        $url .= '&categoria=' . urlencode($categoria);
    }

    header('Location: ' . $url);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ../nueva_categoria.php');
    exit;
}

$categoria = trim((string)($_POST['categoria'] ?? ''));

if ($categoria === '' || strlen($categoria) > 255) {
    redirect_with_error('invalid');
}

$organismo = clean_value($_POST['organismo'] ?? null);
$procesoSelectivo = clean_value($_POST['proceso_selectivo'] ?? null);
$turno = clean_value($_POST['turno'] ?? null);
$tipo = clean_value($_POST['tipo'] ?? null);
$descripcion = clean_value($_POST['descripcion'] ?? null);

$convocatoriaYear = null;
$rawYear = trim((string)($_POST['convocatoria_year'] ?? ''));

if ($rawYear !== '') {
    if (!ctype_digit($rawYear)) {
        redirect_with_error('invalid_year', $categoria);
    }

    $convocatoriaYear = (int)$rawYear;

    if ($convocatoriaYear < 1900 || $convocatoriaYear > 2100) {
        redirect_with_error('invalid_year', $categoria);
    }
}

$stmt = mysqli_prepare($link, "SELECT id FROM question_sets WHERE categoria = ? LIMIT 1");
mysqli_stmt_bind_param($stmt, "s", $categoria);
mysqli_stmt_execute($stmt);
$res = mysqli_stmt_get_result($stmt);
$existing = mysqli_fetch_assoc($res);
mysqli_stmt_close($stmt);

if ($existing) {
    redirect_with_error('duplicate', $categoria);
}

$stmt = mysqli_prepare(
    $link,
    "INSERT INTO question_sets (
        categoria,
        organismo,
        proceso_selectivo,
        convocatoria_year,
        turno,
        tipo,
        descripcion
    ) VALUES (?, ?, ?, ?, ?, ?, ?)"
);

mysqli_stmt_bind_param(
    $stmt,
    "sssisss",
    $categoria,
    $organismo,
    $procesoSelectivo,
    $convocatoriaYear,
    $turno,
    $tipo,
    $descripcion
);

if (!mysqli_stmt_execute($stmt)) {
    mysqli_stmt_close($stmt);
    redirect_with_error('save_failed', $categoria);
}

mysqli_stmt_close($stmt);

$next = $_POST['next'] ?? 'stay';

if ($next === 'add_questions') {
    header('Location: ../agregar.php?created_category=1&categoria=' . urlencode($categoria));
    exit;
}

header('Location: ../nueva_categoria.php?created=1&categoria=' . urlencode($categoria));
exit;
