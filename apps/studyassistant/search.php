<?php

declare(strict_types=1);

require_once __DIR__ . '/includes/autoload.php';

use StudyAssistant\Service\KnowledgeServiceClient;

/**
 * Búsqueda semántica: reenvía la consulta al servicio `embeddings`
 * y devuelve los resultados enlazados a note.php#anchor.
 */

header('Content-Type: application/json; charset=utf-8');

$query = trim((string)($_GET['q'] ?? ''));
$topK = max(1, min((int)($_GET['top_k'] ?? 8), 20));

if ($query === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Falta el parámetro q.'], JSON_UNESCAPED_UNICODE);
    exit;
}

$embeddingsUrl = getenv('EMBEDDINGS_SERVICE_URL') ?: 'http://embeddings:8000';
$client = new KnowledgeServiceClient($embeddingsUrl, 10);

try {
    $data = $client->get('/search', ['q' => $query, 'top_k' => $topK]);

    // Enlace directo a note.php#anchor para cada resultado.
    if (!empty($data['results']) && is_array($data['results'])) {
        foreach ($data['results'] as &$result) {
            $result['url'] = 'note.php?id=' . urlencode((string)$result['note_id'])
                . (!empty($result['anchor']) ? '#' . $result['anchor'] : '');
        }
        unset($result);
    }

    echo json_encode($data, JSON_UNESCAPED_UNICODE);
} catch (Throwable $e) {
    http_response_code(502);
    echo json_encode([
        'error' => 'No se ha podido contactar con el servicio de búsqueda semántica (¿está levantado el contenedor "embeddings"?).',
        'details' => $e->getMessage(),
    ], JSON_UNESCAPED_UNICODE);
}
