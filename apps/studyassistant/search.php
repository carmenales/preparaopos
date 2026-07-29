<?php

/**
 * Búsqueda semántica: reenvía la consulta al servicio `embeddings`
 * (ver docker-compose.yml, servicio interno, sin coste ni API externa)
 * y devuelve los resultados enlazados a note.php#anchor.
 *
 * Igual que ai_client.php: sin cURL, con file_get_contents + stream
 * context, para no añadir dependencias a la imagen PHP.
 */

header('Content-Type: application/json; charset=utf-8');

const SA_EMBEDDINGS_SERVICE_URL = 'http://embeddings:8000';
const SA_SEARCH_TIMEOUT_SECONDS = 10;

function sa_search_respond(int $httpCode, array $body): void
{
    http_response_code($httpCode);
    echo json_encode($body, JSON_UNESCAPED_UNICODE);
    exit;
}

$query = trim((string) ($_GET['q'] ?? ''));
$topK = (int) ($_GET['top_k'] ?? 8);
$topK = max(1, min($topK, 20));

if ($query === '') {
    sa_search_respond(400, ['error' => 'Falta el parámetro q.']);
}

$url = SA_EMBEDDINGS_SERVICE_URL . '/search?' . http_build_query([
    'q' => $query,
    'top_k' => $topK,
]);

$context = stream_context_create([
    'http' => [
        'method' => 'GET',
        'timeout' => SA_SEARCH_TIMEOUT_SECONDS,
        'ignore_errors' => true, // para poder leer el cuerpo de error del servicio
    ],
]);

$raw = @file_get_contents($url, false, $context);

if ($raw === false) {
    sa_search_respond(502, [
        'error' => 'No se ha podido contactar con el servicio de búsqueda semántica '
            . '(¿está levantado el contenedor "embeddings"? -> docker compose up embeddings).',
    ]);
}

$statusLine = $http_response_header[0] ?? '';
$statusCode = 0;
if (preg_match('/\s(\d{3})\s/', $statusLine, $matches)) {
    $statusCode = (int) $matches[1];
}

$data = json_decode($raw, true);

if ($statusCode !== 200 || !is_array($data)) {
    sa_search_respond(502, [
        'error' => 'El servicio de búsqueda semántica ha devuelto un error.',
        'details' => $data['detail'] ?? $raw,
    ]);
}

// Enlace directo a note.php#anchor para cada resultado.
if (!empty($data['results']) && is_array($data['results'])) {
    foreach ($data['results'] as &$result) {
        $result['url'] = 'note.php?id=' . urlencode($result['note_id'])
            . ($result['anchor'] ? '#' . $result['anchor'] : '');
    }
    unset($result);
}

sa_search_respond(200, $data);
