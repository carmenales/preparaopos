<?php

declare(strict_types=1);

/**
 * Autoloader PSR-4 ultraligero y nativo para StudyAssistant.
 * Mapea el namespace 'StudyAssistant\' al directorio 'apps/studyassistant/src/'.
 */
spl_autoload_register(static function (string $class): void {
    $prefix = 'StudyAssistant\\';
    $baseDir = __DIR__ . '/../src/';

    $len = strlen($prefix);
    if (strncmp($prefix, $class, $len) !== 0) {
        return;
    }

    $relativeClass = substr($class, $len);
    $file = $baseDir . str_replace('\\', '/', $relativeClass) . '.php';

    if (is_file($file)) {
        require_once $file;
    }
});

