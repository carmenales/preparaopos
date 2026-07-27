<?php

$appsConfig = require __DIR__ . '/../config/apps.php';

function app_config(): array
{
    global $appsConfig;
    return $appsConfig;
}

function get_tai_url(string $path = ''): string
{
    $config = app_config();
    return rtrim($config['preparadortai_url'], '/') . '/' . ltrim($path, '/');
}

function get_studyassistant_url(string $path = ''): string
{
    $config = app_config();
    return rtrim($config['studyassistant_url'], '/') . '/' . ltrim($path, '/');
}

function build_studyassistant_note_url(string $id): string
{
    return get_studyassistant_url('note.php?id=' . rawurlencode($id));
}

function build_preparadortai_topic_practice_url(array $topics, array $context = []): string
{
    $query = [
        'topics' => array_values(array_filter($topics, static function ($value) {
            return trim((string)$value) !== '';
        })),
    ];

    foreach ($context as $key => $value) {
        if ($value === null || $value === '') {
            continue;
        }

        $query[$key] = is_array($value) ? implode(',', $value) : $value;
    }

    return get_tai_url('practica_tematica.php?' . http_build_query($query));
}