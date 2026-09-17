<?php
require_once __DIR__ . '/includes/knowledge.php';
require_once __DIR__ . '/includes/markdown.php';
require_once __DIR__ . '/../shared/helpers/url.php';

$notes = sa_load_index();
$id = isset($_GET['id']) ? trim($_GET['id']) : '';
$note = sa_find_note_by_id($notes, $id);
$markdown = null;
$error = null;

if (!$note) {
    $error = 'No se ha encontrado el apunte solicitado.';
} else {
    $absolutePath = sa_note_absolute_path($note);

    if ($absolutePath === null || !is_file($absolutePath)) {
        $error = 'No se ha podido abrir el fichero Markdown asociado.';
    } else {
        $markdown = file_get_contents($absolutePath);
    }
}

$topicQueries = [];

if (!empty($note['official_topic'])) {
    if (preg_match('/Tema\s+\d+\.\s*(.+)$/i', $note['official_topic'], $matches)) {
        $topicQueries[] = trim($matches[1]);
    } else {
        $topicQueries[] = trim($note['official_topic']);
    }
}

$renderedContent = '';
if ($markdown !== null) {
    $renderedContent = sa_render_markdown($markdown, $id);
    $renderedContent = add_heading_anchors($renderedContent);
}

$headings = $note['headings'] ?? [];

// Temas sugeridos para práctica (practice.topics, tags, official_topic)
$practiceTopics = sa_normalize_practice_topics($note);

// Proceso actual para navegación contextual y secuencial
$currentProcess = isset($_GET['process']) && trim($_GET['process']) !== '' ? trim($_GET['process']) : null;
if ($currentProcess === null && !empty($note['processes']) && is_array($note['processes'])) {
    $currentProcess = (string)$note['processes'][0];
}

$siblingNotes = [];
if ($currentProcess !== null) {
    foreach ($notes as $n) {
        if (!empty($n['processes']) && in_array($currentProcess, $n['processes'], true)) {
            $siblingNotes[] = $n;
        }
    }
    sa_sort_notes_sequentially($siblingNotes);
}

$currentIndex = -1;
$prevNote = null;
$nextNote = null;
$totalSiblings = count($siblingNotes);
$currentPosition = 0;
$progressPercent = 0;

if ($totalSiblings > 0) {
    foreach ($siblingNotes as $idx => $sNote) {
        if ((string)($sNote['id'] ?? '') === (string)$id) {
            $currentIndex = $idx;
            break;
        }
    }

    if ($currentIndex !== -1) {
        $currentPosition = $currentIndex + 1;
        $progressPercent = (int)round(($currentPosition / $totalSiblings) * 100);
        if ($currentIndex > 0) {
            $prevNote = $siblingNotes[$currentIndex - 1];
        }
        if ($currentIndex < $totalSiblings - 1) {
            $nextNote = $siblingNotes[$currentIndex + 1];
        }
    }
}

// --- LÓGICA DE TOC ANIDADO ---
function build_nested_toc(array $headings) {
    $tree = [];
    $stack = [];

    foreach ($headings as $h) {
        if ($h['level'] < 2 || $h['level'] > 4) {
            continue;
        }

        $node = ['heading' => $h, 'children' => []];

        while (!empty($stack) && $stack[count($stack) - 1]['heading']['level'] >= $h['level']) {
            array_pop($stack);
        }

        if (empty($stack)) {
            $tree[] = &$node;
        } else {
            $stack[count($stack) - 1]['children'][] = &$node;
        }

        $stack[] = &$node;
        unset($node);
    }

    return $tree;
}

function render_nested_toc(array $tree) {
    if (empty($tree)) {
        return '';
    }

    $html = '<ul class="nested-toc-list">';

    foreach ($tree as $node) {
        $h = $node['heading'];
        $children = $node['children'];
        $html .= '<li class="toc-item level-' . (int)$h['level'] . '">';

        if (!empty($children)) {
            $html .= '<details open class="toc-details">';
            $html .= '<summary class="toc-summary">';
            // El stopPropagation evita que al pulsar el enlace se cierre la carpeta
            $html .= '<a href="#' . htmlspecialchars($h['anchor'], ENT_QUOTES, 'UTF-8') . '" onclick="event.stopPropagation()">' . sa_safe_text($h['text']) . '</a>';
            $html .= '</summary>';
            $html .= render_nested_toc($children);
            $html .= '</details>';
        } else {
            $html .= '<div class="toc-link-wrapper">';
            $html .= '<a href="#' . htmlspecialchars($h['anchor'], ENT_QUOTES, 'UTF-8') . '">' . sa_safe_text($h['text']) . '</a>';
            $html .= '</div>';
        }

        $html .= '</li>';
    }

    $html .= '</ul>';

    return $html;
}

$nestedTocTree = build_nested_toc($headings);
$nestedTocHtml = render_nested_toc($nestedTocTree);
$pageTitle = $note['title'] ?? 'Apunte';
require __DIR__ . '/includes/header.php';
?>

<?php if ($error): ?>
    <div class="alert"><?php echo sa_safe_text($error); ?></div>
    <p><a class="button-secondary" href="index.php">Volver al listado</a></p>
<?php else: ?>

    <!-- Ruta de navegación (Breadcrumbs) -->
    <nav class="note-breadcrumbs" aria-label="Ruta de navegación">
        <ol class="breadcrumb-list">
            <li class="breadcrumb-item">
                <a href="index.php" class="breadcrumb-link" title="Ir al inicio de Study Assistant">
                    <span>🏠 Inicio</span>
                </a>
            </li>
            <?php if (!empty($currentProcess)): ?>
                <li class="breadcrumb-separator" aria-hidden="true">›</li>
                <li class="breadcrumb-item">
                    <a href="index.php?process=<?php echo urlencode($currentProcess); ?>" class="breadcrumb-link" title="Ver temario completo de este proceso">
                        <?php echo sa_safe_text(sa_format_process_title($currentProcess)); ?>
                    </a>
                </li>
            <?php endif; ?>
            <li class="breadcrumb-separator" aria-hidden="true">›</li>
            <li class="breadcrumb-item breadcrumb-current" aria-current="page" title="<?php echo sa_safe_text($note['title'] ?? ''); ?>">
                <?php echo sa_safe_text(!empty($note['official_topic']) ? $note['official_topic'] : ($note['title'] ?? 'Apunte')); ?>
            </li>
        </ol>
    </nav>

    <!-- Contenedor Grid estricto de 2 columnas -->
    <div class="note-layout">
        <aside class="note-sidebar">
            <?php if (!empty($currentProcess)): ?>
                <a class="button-secondary button-back" href="index.php?process=<?php echo urlencode($currentProcess); ?>" title="Volver al temario de <?php echo sa_safe_text(sa_format_process_title($currentProcess)); ?>">
                    ← Volver al temario
                </a>
            <?php else: ?>
                <a class="button-secondary button-back" href="index.php">← Volver al listado</a>
            <?php endif; ?>

            <?php if (!empty($practiceTopics)): ?>
                <div class="note-actions" style="margin: 1.2rem 0;">
                    <a
                        class="button-primary"
                        style="width: 88%; text-align: center; display: block;"
                        href="<?= htmlspecialchars(build_preparadortai_topic_practice_url(
                            $practiceTopics,
                            [
                                'source' => 'studyassistant',
                                'note' => $note['id'] ?? '',
                                // en el futuro puedes volver a añadir 'processes' y 'profiles' si quieres rastreo más fino
                            ]
                        )) ?>"
                    > 📝 Ponerme a prueba
                    </a>
                </div>
                
            <?php endif; ?>
            <div class="note-actions" style="margin: 0.8rem 0;">
                <button
                    type="button"
                    class="button-secondary"
                    style="width: 100%; text-align: center; display: block;"
                    onclick="window.print()"
                >
                    🖨️ Imprimir
                </button>
            </div>

            <?php if (!empty($nestedTocTree)): ?>
                <div class="note-toc-container desktop-only">
                    <h3 style="margin-top: 0; margin-bottom: 12px;">Índice</h3>
                    <nav class="note-toc">
                        <?php echo $nestedTocHtml; ?>
                    </nav>
                </div>
            <?php endif; ?>

            <div class="note-meta-container" style="margin-top: 24px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                <h3 style="margin-top: 0;">Metadatos</h3>
                <dl>
                    <dt>ID</dt>
                    <dd><code><?php echo sa_safe_text($note['id']); ?></code></dd>

                    <?php if (!empty($note['official_topic'])): ?>
                        <dt>Tema oficial</dt>
                        <dd><?php echo sa_safe_text($note['official_topic']); ?></dd>
                    <?php endif; ?>

                    <?php if (!empty($note['status'])): ?>
                        <dt>Estado</dt>
                        <dd><?php echo sa_safe_text($note['status']); ?></dd>
                    <?php endif; ?>

                    <?php if (!empty($note['processes'])): ?>
                        <dt>Procesos</dt>
                        <dd>
                            <?php foreach ($note['processes'] as $proc): ?>
                                <div style="margin-bottom: 6px;">
                                    <a
                                        href="note.php?id=<?php echo urlencode($note['id']); ?>&amp;process=<?php echo urlencode($proc); ?>"
                                        class="<?php echo $proc === $currentProcess ? 'active-process-link' : ''; ?>"
                                        title="<?php echo $proc === $currentProcess ? 'Proceso actualmente activo para navegación' : 'Cambiar navegación a este proceso'; ?>"
                                    >
                                        <?php echo sa_safe_text(sa_format_process_title($proc)); ?>
                                        <?php if ($proc === $currentProcess): ?>
                                            <span class="active-process-badge">activo</span>
                                        <?php endif; ?>
                                    </a>
                                </div>
                            <?php endforeach; ?>
                        </dd>
                    <?php endif; ?>

                    <?php if (!empty($note['tags'])): ?>
                        <dt>Etiquetas</dt>
                        <dd>
                            <div class="tags">
                                <?php foreach ($note['tags'] as $tag): ?>
                                    <a class="tag" href="index.php?tag=<?php echo urlencode($tag); ?>">
                                        <?php echo sa_safe_text($tag); ?>
                                    </a>
                                <?php endforeach; ?>
                            </div>
                        </dd>
                    <?php endif; ?>
                </dl>
            </div>
        </aside>

        <article class="note-content">
            <?php echo $renderedContent; ?>

            <?php if (!empty($currentProcess) && $totalSiblings > 1): ?>
                <section class="note-pagination-section" aria-label="Navegación secuencial de temas">
                    <div class="note-pagination-header">
                        <div class="pagination-progress-info">
                            <span class="pagination-counter-badge">
                                Tema <strong><?php echo $currentPosition; ?></strong> de <strong><?php echo $totalSiblings; ?></strong>
                            </span>
                            <span class="pagination-process-name">
                                en <strong><?php echo sa_safe_text(sa_format_process_title($currentProcess)); ?></strong>
                            </span>
                        </div>
                        <div class="pagination-progress-bar-wrapper" title="<?php echo $progressPercent; ?>% del temario">
                            <div class="pagination-progress-bar" style="width: <?php echo $progressPercent; ?>%;"></div>
                        </div>
                    </div>

                    <div class="note-pagination-grid">
                        <div class="pagination-col prev">
                            <?php if ($prevNote): ?>
                                <a rel="prev" href="note.php?id=<?php echo urlencode($prevNote['id']); ?>&amp;process=<?php echo urlencode($currentProcess); ?>" class="pagination-card prev-card">
                                    <span class="pagination-direction">← Tema anterior</span>
                                    <?php if (!empty($prevNote['official_topic'])): ?>
                                        <span class="pagination-topic-meta"><?php echo sa_safe_text($prevNote['official_topic']); ?></span>
                                    <?php endif; ?>
                                    <span class="pagination-title"><?php echo sa_safe_text($prevNote['title']); ?></span>
                                </a>
                            <?php else: ?>
                                <a href="index.php?process=<?php echo urlencode($currentProcess); ?>" class="pagination-card overview-card prev-card">
                                    <span class="pagination-direction">← Inicio del temario</span>
                                    <span class="pagination-title">Estás en el primer tema · Ver temario</span>
                                </a>
                            <?php endif; ?>
                        </div>

                        <div class="pagination-col next">
                            <?php if ($nextNote): ?>
                                <a rel="next" href="note.php?id=<?php echo urlencode($nextNote['id']); ?>&amp;process=<?php echo urlencode($currentProcess); ?>" class="pagination-card next-card">
                                    <span class="pagination-direction">Tema siguiente →</span>
                                    <?php if (!empty($nextNote['official_topic'])): ?>
                                        <span class="pagination-topic-meta"><?php echo sa_safe_text($nextNote['official_topic']); ?></span>
                                    <?php endif; ?>
                                    <span class="pagination-title"><?php echo sa_safe_text($nextNote['title']); ?></span>
                                </a>
                            <?php else: ?>
                                <a href="index.php?process=<?php echo urlencode($currentProcess); ?>" class="pagination-card overview-card next-card">
                                    <span class="pagination-direction">🎉 Fin del temario</span>
                                    <span class="pagination-title">¡Has completado el temario! · Ver lista</span>
                                </a>
                            <?php endif; ?>
                        </div>
                    </div>
                </section>
            <?php endif; ?>
        </article>
    </div>
<?php endif; ?>

<?php require __DIR__ . '/includes/footer.php'; ?>