// Ruta: apps/shared/helpers/url.php
<?php

// Cargamos la configuración de las apps
$appsConfig = require __DIR__ . '/../config/apps.php';

/**
 * Genera una URL absoluta hacia PreparadorTAI
 */
function get_tai_url($path = '') {
    global $appsConfig;
    return rtrim($appsConfig['preparadortai_url'], '/') . '/' . ltrim($path, '/');
}

/**
 * Genera una URL absoluta hacia StudyAssistant
 */
function get_study_url($path = '') {
    global $appsConfig;
    return rtrim($appsConfig['studyassistant_url'], '/') . '/' . ltrim($path, '/');
}