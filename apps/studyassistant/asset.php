<?php

require_once __DIR__ . '/includes/knowledge.php';

const SA_ASSET_ALLOWED_EXTENSIONS = [
    'png' => 'image/png',
    'jpg' => 'image/jpeg',
    'jpeg' => 'image/jpeg',
    'gif' => 'image/gif',
    'webp' => 'image/webp',
    'svg' => 'image/svg+xml',
];

function sa_asset_fail(int $httpCode, string $message): void
{
    http_response_code($httpCode);
    header('Content-Type: text/plain; charset=utf-8');
    echo $message;
    exit;
}

$noteId = isset($_GET['note']) ? trim($_GET['note']) : '';
$relativePath = isset($_GET['path']) ? trim($_GET['path']) : '';

if ($noteId === '' || $relativePath === '') {
    sa_asset_fail(400, 'Faltan parámetros note/path.');
}

$relativePath = str_replace('\\', '/', $relativePath);
$relativePath = urldecode($relativePath);

if ($relativePath === '' || $relativePath[0] === '/' || preg_match('#^([A-Za-z]:)?/#', $relativePath)) {
    sa_asset_fail(400, 'Ruta no permitida.');
}

$extension = strtolower(pathinfo($relativePath, PATHINFO_EXTENSION));
if (!isset(SA_ASSET_ALLOWED_EXTENSIONS[$extension])) {
    sa_asset_fail(400, 'Tipo de fichero no permitido.');
}

$notes = sa_load_index();
$note = sa_find_note_by_id($notes, $noteId);

if (!$note) {
    sa_asset_fail(404, 'Apunte no encontrado.');
}

$noteAbsolutePath = sa_note_absolute_path($note);
if ($noteAbsolutePath === null) {
    sa_asset_fail(404, 'No se ha podido resolver el apunte.');
}

$knowledgeBasePath = realpath(sa_project_base_path() . '/knowledge');
$candidatePath = realpath(dirname($noteAbsolutePath) . '/' . $relativePath);

if (
    $candidatePath === false
    || $knowledgeBasePath === false
    || strpos($candidatePath, $knowledgeBasePath) !== 0
    || !is_file($candidatePath)
) {
    sa_asset_fail(404, 'Fichero no encontrado.');
}

header('Content-Type: ' . SA_ASSET_ALLOWED_EXTENSIONS[$extension]);
header('Cache-Control: public, max-age=86400');
header('Content-Length: ' . filesize($candidatePath));
readfile($candidatePath);
