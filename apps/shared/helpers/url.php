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