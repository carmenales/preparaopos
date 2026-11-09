<?php

declare(strict_types=1);

/**
 * Suite de pruebas de verificación para la refactorización OOP de StudyAssistant.
 * Ejecutable dentro del contenedor:
 * php /workspace/apps/studyassistant/tests/test_studyassistant.php
 */

$appDir = dirname(__DIR__);

require_once $appDir . '/includes/autoload.php';
require_once $appDir . '/includes/knowledge.php';
require_once $appDir . '/includes/markdown.php';

use StudyAssistant\Knowledge\NoteRepository;
use StudyAssistant\Markdown\MarkdownRenderer;
use StudyAssistant\Navigation\TableOfContents;
use StudyAssistant\Dashboard\DashboardMetrics;
use StudyAssistant\Service\KnowledgeServiceClient;

$passed = 0;
$failed = 0;

function assert_true(bool $condition, string $testName): void
{
    global $passed, $failed;
    if ($condition) {
        echo "  [PASS] {$testName}\n";
        $passed++;
    } else {
        echo "  [FAIL] {$testName}\n";
        $failed++;
    }
}

function assert_equals(mixed $expected, mixed $actual, string $testName): void
{
    global $passed, $failed;
    if ($expected === $actual) {
        echo "  [PASS] {$testName}\n";
        $passed++;
    } else {
        echo "  [FAIL] {$testName} (Expected: " . json_encode($expected) . ", Got: " . json_encode($actual) . ")\n";
        $failed++;
    }
}

echo "=== 1. TEST: Autoloader ===\n";
assert_true(class_exists(NoteRepository::class), 'NoteRepository class is autoloaded');
assert_true(class_exists(MarkdownRenderer::class), 'MarkdownRenderer class is autoloaded');
assert_true(class_exists(TableOfContents::class), 'TableOfContents class is autoloaded');
assert_true(class_exists(DashboardMetrics::class), 'DashboardMetrics class is autoloaded');
assert_true(class_exists(KnowledgeServiceClient::class), 'KnowledgeServiceClient class is autoloaded');

echo "\n=== 2. TEST: NoteRepository ===\n";
$repo = NoteRepository::getInstance();
assert_true($repo instanceof NoteRepository, 'Singleton NoteRepository instance');

// Mock notes for testing logic independent of filesystem
$mockNotes = [
    [
        'id' => 'note-1',
        'title' => 'Esquema Nacional de Seguridad',
        'official_topic' => 'Tema 10. Seguridad',
        'excerpt' => 'El ENS establece los principios básicos...',
        'content_text' => 'Contenido detallado de seguridad...',
        'tags' => ['seguridad', 'ens', 'ciberseguridad'],
        'processes' => ['age/a2-gsi', 'age/c1-tai'],
        'status' => 'revisado',
        'path' => 'knowledge/processes/age/a2-gsi/ens.md',
        'headings' => [
            ['level' => 2, 'text' => 'Principios Básicos', 'anchor' => 'principios-basicos'],
            ['level' => 3, 'text' => 'Seguridad integral', 'anchor' => 'seguridad-integral'],
            ['level' => 2, 'text' => 'Dimensiones de Seguridad', 'anchor' => 'dimensiones-de-seguridad'],
        ],
        'practice' => ['topics' => ['10', 'Seguridad TIC']],
    ],
    [
        'id' => 'note-2',
        'title' => 'Constitución Española',
        'official_topic' => 'Tema 1. Derecho Constitucional',
        'excerpt' => 'La Constitución de 1978...',
        'content_text' => 'Título preliminar...',
        'tags' => ['constitucion', 'derecho'],
        'processes' => ['age/a2-gsi'],
        'status' => 'borrador',
        'path' => 'knowledge/processes/age/a2-gsi/constitucion.md',
        'headings' => [
            ['level' => 2, 'text' => 'Título Preliminar', 'anchor' => 'titulo-preliminar'],
        ],
    ],
];

$found = $repo->findById('note-1', $mockNotes);
assert_true($found !== null && $found['id'] === 'note-1', 'findById finds existing note');

$notFound = $repo->findById('inexistente', $mockNotes);
assert_true($notFound === null, 'findById returns null for non-existent note');

$filtered = $repo->filter('seguridad', '', '', '', $mockNotes);
assert_equals(1, count($filtered), 'filter by query string');

$filteredByTag = $repo->filter('', 'constitucion', '', '', $mockNotes);
assert_equals(1, count($filteredByTag), 'filter by tag');

$filteredByStatus = $repo->filter('', '', '', 'revisado', $mockNotes);
assert_equals(1, count($filteredByStatus), 'filter by status');

$byProcess = $repo->getByProcess('age/a2-gsi', $mockNotes);
assert_equals(2, count($byProcess), 'getByProcess returns matching notes');

$byProcessNone = $repo->getByProcess('proceso-inexistente', $mockNotes);
assert_equals(0, count($byProcessNone), 'getByProcess returns empty for non-existent process');

$uniqueTags = $repo->collectUnique('tags', $mockNotes);
assert_true(in_array('seguridad', $uniqueTags, true) && in_array('constitucion', $uniqueTags, true), 'collectUnique tags');

$uniqueStatuses = $repo->collectStatuses($mockNotes);
assert_equals(['borrador', 'revisado'], $uniqueStatuses, 'collectStatuses');

$practiceTopics = $repo->normalizePracticeTopics($mockNotes[0]);
assert_equals(['10', 'Seguridad TIC'], $practiceTopics, 'normalizePracticeTopics from practice.topics');

$practiceTopicsFallback = $repo->normalizePracticeTopics($mockNotes[1]);
assert_equals(['constitucion', 'derecho'], $practiceTopicsFallback, 'normalizePracticeTopics fallback to tags');

$pretty = $repo->prettifySlug('age/a2-gsi');
assert_true(strpos($pretty, 'AGE') !== false || strpos($pretty, 'A2-GSI') !== false, 'prettifySlug handles acronyms');

$readingTime = $repo->estimateReadingTime($mockNotes[0]);
assert_true(strpos($readingTime, 'min') !== false, 'estimateReadingTime format');

$badgeRevisado = $repo->statusBadgeClass('revisado');
assert_equals('badge-status-revisado', $badgeRevisado, 'statusBadgeClass revisado');

$badgeBorrador = $repo->statusBadgeClass('borrador');
assert_equals('badge-status-borrador', $badgeBorrador, 'statusBadgeClass borrador');

// Test sequential sorting
$toSort = [$mockNotes[0], $mockNotes[1]];
$repo->sortSequentially($toSort);
assert_equals('note-2', $toSort[0]['id'], 'sortSequentially sorts Tema 1 before Tema 10');

// Test path traversal security
$safeNote = ['path' => 'knowledge/processes/age/a2-gsi/ens.md'];
$maliciousNote = ['path' => '../../../../etc/passwd'];
$evilResult = $repo->getAbsolutePath($maliciousNote);
assert_true($evilResult === null, 'getAbsolutePath blocks path traversal attack');

echo "\n=== 3. TEST: MarkdownRenderer ===\n";
$renderer = new MarkdownRenderer('test-note');

// Inline rendering
$inlineBold = $renderer->renderInline('Este es un texto con **negrita** y *cursiva*.');
assert_true(strpos($inlineBold, '<strong>negrita</strong>') !== false, 'renderInline renders bold');
assert_true(strpos($inlineBold, '<em>cursiva</em>') !== false, 'renderInline renders italic');

// MathJax
$inlineMath = $renderer->renderInline('La fórmula es $E = mc^2$');
assert_true(strpos($inlineMath, '<span class="math-inline">\\(E = mc^2\\)</span>') !== false, 'renderInline MathJax formula');

$blockMath = $renderer->render("$$\n\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\n$$");
assert_true(strpos($blockMath, '<div class="math-block">') !== false, 'render block MathJax formula');

// Mermaid
$mermaid = $renderer->render("```mermaid\ngraph TD;\nA-->B;\n```");
assert_true(strpos($mermaid, '<pre class="mermaid">') !== false, 'render Mermaid block');

// Quiz Card
$quiz = $renderer->render("Pregunta 1. ¿Cuál es el puerto HTTP por defecto?\nA) 21\nB) 80\nC) 443\n**Respuesta correcta: B**");
assert_true(strpos($quiz, 'class="quiz-card"') !== false, 'render Quiz card container');
assert_true(strpos($quiz, 'Pregunta 1') !== false, 'render Quiz card label');
assert_true(strpos($quiz, 'Mostrar respuesta y explicación') !== false, 'render Quiz card answer details');

// Table
$table = $renderer->render("| Cabecera 1 | Cabecera 2 |\n| --- | --- |\n| Valor A | Valor B |");
assert_true(strpos($table, '<div class="table-wrapper"><table>') !== false, 'render GFM table');

// Heading anchors
$anchored = $renderer->addHeadingAnchors('<h2 id="mi-seccion">Mi Sección</h2>');
assert_true(strpos($anchored, 'href="#mi-seccion"') !== false, 'addHeadingAnchors adds anchor link');
assert_true(strpos($anchored, 'class="heading-anchor"') !== false, 'addHeadingAnchors has correct class');

echo "\n=== 4. TEST: TableOfContents ===\n";
$toc = new TableOfContents();
$headings = [
    ['level' => 2, 'text' => 'Sección 1', 'anchor' => 'sec-1'],
    ['level' => 3, 'text' => 'Subsección 1.1', 'anchor' => 'sec-1-1'],
    ['level' => 3, 'text' => 'Subsección 1.2', 'anchor' => 'sec-1-2'],
    ['level' => 2, 'text' => 'Sección 2', 'anchor' => 'sec-2'],
];

$tree = $toc->buildTree($headings);
assert_equals(2, count($tree), 'buildTree creates top-level items');
assert_equals(2, count($tree[0]['children']), 'buildTree nests children under h2');

$tocHtml = $toc->renderTree($tree);
assert_true(strpos($tocHtml, 'class="nested-toc-list"') !== false, 'renderTree produces nested-toc-list');
assert_true(strpos($tocHtml, '<details open class="toc-details">') !== false, 'renderTree produces collapsible details for items with children');
assert_true(strpos($tocHtml, 'href="#sec-1"') !== false, 'renderTree includes anchor links');

echo "\n=== 5. TEST: DashboardMetrics ===\n";
$metrics = new DashboardMetrics($mockNotes, ['age/a2-gsi'], ['seguridad', 'constitucion'], $repo);
assert_equals(2, $metrics->getTotalNotes(), 'DashboardMetrics total notes');
assert_equals(1, $metrics->getTotalProcesses(), 'DashboardMetrics total processes');
assert_equals(2, $metrics->getTotalTags(), 'DashboardMetrics total tags');
assert_equals(1, $metrics->getReviewedCount(), 'DashboardMetrics reviewed count');
assert_equals(1, $metrics->getDraftCount(), 'DashboardMetrics draft count');

$summaries = $metrics->getProcessSummaries();
assert_true(isset($summaries['age/a2-gsi']), 'DashboardMetrics process summary exists');
assert_equals(2, $summaries['age/a2-gsi']['total'], 'DashboardMetrics process summary total');
assert_equals(1, $summaries['age/a2-gsi']['reviewed'], 'DashboardMetrics process summary reviewed');
assert_equals(1, $summaries['age/a2-gsi']['draft'], 'DashboardMetrics process summary draft');

$activeFilters = $metrics->buildActiveFilters(['q' => 'seguridad', 'process' => 'age/a2-gsi'], 'seguridad', 'age/a2-gsi', '', '');
assert_equals(2, count($activeFilters), 'buildActiveFilters generates correct number of chips');

echo "\n=== 6. TEST: KnowledgeServiceClient ===\n";
$client = new KnowledgeServiceClient('http://custom-host:9999');
assert_equals('http://custom-host:9999', $client->getBaseUrl(), 'KnowledgeServiceClient custom URL');

$defaultClient = new KnowledgeServiceClient();
assert_true(strpos($defaultClient->getBaseUrl(), 'http://') === 0, 'KnowledgeServiceClient default URL starts with http://');

echo "\n=== 7. TEST: Backward-Compatible Facade Functions ===\n";
assert_true(function_exists('sa_load_index'), 'sa_load_index exists');
assert_true(function_exists('sa_find_note_by_id'), 'sa_find_note_by_id exists');
assert_true(function_exists('sa_note_absolute_path'), 'sa_note_absolute_path exists');
assert_true(function_exists('sa_filter_notes'), 'sa_filter_notes exists');
assert_true(function_exists('sa_collect_unique'), 'sa_collect_unique exists');
assert_true(function_exists('sa_format_process_title'), 'sa_format_process_title exists');
assert_true(function_exists('sa_render_markdown'), 'sa_render_markdown exists');
assert_true(function_exists('add_heading_anchors'), 'add_heading_anchors exists');
assert_true(function_exists('build_nested_toc'), 'build_nested_toc exists');
assert_true(function_exists('render_nested_toc'), 'render_nested_toc exists');

// Facade execution checks
$facadeFound = sa_find_note_by_id($mockNotes, 'note-1');
assert_equals('note-1', $facadeFound['id'], 'sa_find_note_by_id facade returns correct note');

$facadeFiltered = sa_filter_notes($mockNotes, 'seguridad', '', '', '');
assert_equals(1, count($facadeFiltered), 'sa_filter_notes facade filters correctly');

$facadeTocTree = build_nested_toc($headings);
assert_equals(2, count($facadeTocTree), 'build_nested_toc facade returns tree');

$facadeTocHtml = render_nested_toc($facadeTocTree);
assert_true(strpos($facadeTocHtml, 'nested-toc-list') !== false, 'render_nested_toc facade renders HTML');

echo "\n=========================================\n";
echo "Results: {$passed} passed, {$failed} failed\n";
echo "=========================================\n";

if ($failed > 0) {
    exit(1);
}

