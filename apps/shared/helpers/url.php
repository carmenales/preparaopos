<?php

$appsConfig = require __DIR__ . '/../config/apps.php';

function get_tai_url($path = '') {
    global $appsConfig;
    return rtrim($appsConfig['preparadortai_url'], '/') . '/' . ltrim($path, '/');
}

function get_study_url($path = '') {
    global $appsConfig;
    return rtrim($appsConfig['studyassistant_url'], '/') . '/' . ltrim($path, '/');
}

function app_config(): array {
    global $appsConfig;
    return $appsConfig;
}

function build_studyassistant_note_url(string $slug): string {
    return get_study_url('note.php?id=' . rawurlencode($slug));
}

function build_preparadortai_topic_practice_url(array $topics, array $context = []): string {
    $query = [
        // http_build_query convertirá automáticamente esto en topics[0]=...&topics[1]=...
        'topics' => $topics,
    ];
    
    foreach ($context as $key => $value) {
        if ($value === null || $value === '') {
            continue;
        }
        $query[$key] = is_array($value) ? implode(',', $value) : $value;
    }
    
    return get_tai_url('practica_tematica.php?' . http_build_query($query));
}