<?php
$currentTitle = $pageTitle ?? 'Study Assistant';
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title><?php echo sa_safe_text($currentTitle); ?></title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="assets/styles.css" rel="stylesheet">
</head>
<body>
<header class="topbar">
    <div>
        <a class="brand" href="index.php">Study Assistant</a>
        <span class="subtitle">Base de conocimiento Markdown</span>
    </div>
    <nav>
        <a href="index.php">Apuntes</a>
    </nav>
</header>
<main class="container">
