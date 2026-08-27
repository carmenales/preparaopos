<?php
$currentTitle = $pageTitle ?? 'Study Assistant';
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title><?php echo sa_safe_text($currentTitle); ?></title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['\\(', '\\)']],
                displayMath: [['\\[', '\\]']],
                processEscapes: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
            }
        };
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

        mermaid.initialize({
            startOnLoad: false,
            securityLevel: 'loose',
            theme: 'base',
            themeVariables: {
                darkMode: false,
                background: '#ffffff',
                primaryColor: '#e0f2fe',
                primaryTextColor: '#0f172a',
                primaryBorderColor: '#38bdf8',
                lineColor: '#0ea5e9',
                secondaryColor: '#ecfeff',
                tertiaryColor: '#fef3c7',
                textColor: '#0f172a',
                mainBkg: '#ffffff',
                nodeBorder: '#38bdf8',
                clusterBkg: '#ffffff',
                clusterBorder: '#dfe6ee',
                defaultLinkColor: '#0ea5e9',
                fontFamily: 'system-ui, sans-serif'
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
            mermaid.run({
                nodes: document.querySelectorAll('.mermaid'),
                suppressErrors: true
            });
        });
    </script>

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
