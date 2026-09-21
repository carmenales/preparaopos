<?php

declare(strict_types=1);

namespace StudyAssistant\Service;

use CURLFile;
use RuntimeException;

/**
 * Cliente HTTP/cURL para interactuar con el microservicio de conocimiento y embeddings.
 * Encapsula la extracción de PDFs, refinado de Markdown con LLMs, publicación de apuntes
 * y búsquedas semánticas con timeouts configurables y manejo de errores estructurado.
 */
class KnowledgeServiceClient
{
    private string $baseUrl;
    private int $defaultTimeout;

    public function __construct(?string $baseUrl = null, int $defaultTimeout = 60)
    {
        $this->baseUrl = rtrim($baseUrl ?? (getenv('KNOWLEDGE_SERVICE_URL') ?: 'http://knowledge-service:8000'), '/');
        $this->defaultTimeout = $defaultTimeout;
    }

    public function getBaseUrl(): string
    {
        return $this->baseUrl;
    }

    /**
     * Extrae texto estructurado y headings de un fichero PDF.
     *
     * @param string $filePath Ruta local temporal del archivo PDF.
     * @param string $originalName Nombre original del archivo.
     * @param bool $normalize Si se debe normalizar el texto (unión de guiones, limpieza de saltos espurios).
     * @param int $timeout Tiempo máximo de espera en segundos (por defecto 180s).
     * @return array Datos extraídos estructurados (markdown, headings, metadata, etc.).
     * @throws RuntimeException Si la conexión falla o el microservicio devuelve un error.
     */
    public function extractPdf(string $filePath, string $originalName, bool $normalize = true, int $timeout = 180): array
    {
        if (!is_file($filePath)) {
            throw new RuntimeException("El archivo PDF a procesar no existe en: {$filePath}");
        }

        $postData = [
            'file' => new CURLFile($filePath, 'application/pdf', $originalName),
            'normalize' => $normalize ? 'true' : 'false',
        ];

        return $this->postMultipart('/ingest/extract-pdf', $postData, $timeout);
    }

    /**
     * Envía contenido Markdown para refinado o estructuración asistida por LLM.
     *
     * @param array $payload Datos a enviar (markdown, prompt, etc.).
     * @param int $timeout Tiempo máximo de espera en segundos (por defecto 300s para LLM).
     * @return array Resultado del refinado devuelto por el servicio.
     * @throws RuntimeException
     */
    public function refine(array $payload, int $timeout = 300): array
    {
        return $this->postJson('/ingest/refine', $payload, $timeout);
    }

    /**
     * Publica un apunte de forma definitiva en la base de conocimiento.
     *
     * @param array $payload Metadatos y contenido Markdown del apunte.
     * @param int $timeout Tiempo máximo de espera en segundos (por defecto 60s).
     * @return array Respuesta de confirmación del servicio de conocimiento.
     * @throws RuntimeException
     */
    public function publish(array $payload, int $timeout = 60): array
    {
        return $this->postJson('/ingest/publish', $payload, $timeout);
    }

    /**
     * Realiza una petición GET con query parameters.
     *
     * @throws RuntimeException
     */
    public function get(string $endpoint, array $params = [], int $timeout = 10): array
    {
        $queryString = !empty($params) ? '?' . http_build_query($params) : '';
        return $this->request('GET', $endpoint . $queryString, null, [], $timeout);
    }

    /**
     * Envía una petición POST con payload JSON.
     *
     * @throws RuntimeException
     */
    public function postJson(string $endpoint, array $data, int $timeout = 60): array
    {
        $json = json_encode($data, JSON_UNESCAPED_UNICODE);
        if ($json === false) {
            throw new RuntimeException('Error al codificar el payload a JSON.');
        }

        return $this->request('POST', $endpoint, $json, ['Content-Type: application/json'], $timeout);
    }

    /**
     * Envía una petición POST multipart (para carga de ficheros).
     *
     * @throws RuntimeException
     */
    public function postMultipart(string $endpoint, array $postData, int $timeout = 60): array
    {
        return $this->request('POST', $endpoint, $postData, [], $timeout);
    }

    /**
     * Ejecuta la petición cURL y procesa la respuesta.
     *
     * @throws RuntimeException
     */
    private function request(string $method, string $endpoint, mixed $body, array $headers, int $timeout): array
    {
        $url = $this->baseUrl . $endpoint;
        $ch = curl_init($url);

        $options = [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => $timeout,
            CURLOPT_CUSTOMREQUEST => $method,
        ];

        if ($method === 'POST') {
            $options[CURLOPT_POST] = true;
            $options[CURLOPT_POSTFIELDS] = $body;
        }

        if (!empty($headers)) {
            $options[CURLOPT_HTTPHEADER] = $headers;
        }

        curl_setopt_array($ch, $options);

        $rawResponse = curl_exec($ch);
        $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        if ($curlError) {
            throw new RuntimeException("Error de conexión con el servicio de conocimiento ({$url}): {$curlError}");
        }

        $decoded = json_decode((string)$rawResponse, true);

        if ($httpCode >= 400) {
            $message = is_array($decoded) && isset($decoded['detail'])
                ? (is_string($decoded['detail']) ? $decoded['detail'] : json_encode($decoded['detail'], JSON_UNESCAPED_UNICODE))
                : "Error HTTP {$httpCode} devuelto por el servicio.";
            throw new RuntimeException($message, $httpCode);
        }

        if (!is_array($decoded)) {
            throw new RuntimeException("Respuesta inesperada del servicio (no es un objeto/array JSON válido): " . substr((string)$rawResponse, 0, 200));
        }

        return $decoded;
    }
}

