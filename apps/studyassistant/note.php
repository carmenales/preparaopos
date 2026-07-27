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
    $renderedContent = sa_render_markdown($markdown);
    $renderedContent = add_heading_anchors($renderedContent);
}

$headings = $note['headings'] ?? [];

// --- LÓGICA DE TOC ANIDADO ---
function build_nested_toc(array $headings) {
    $tree = [];
    $stack = [];
    foreach ($headings as $h) {
        if ($h['level'] < 2 || $h['level'] > 4) continue;
        $node = ['heading' => $h, 'children' => []];
        
        while (!empty($stack) && $stack[count($stack)-1]['heading']['level'] >= $h['level']) {
            array_pop($stack);
        }
        
        if (empty($stack)) {
            $tree[] = &$node;
        } else {
            $stack[count($stack)-1]['children'][] = &$node;
        }
        
        $stack[] = &$node;
        unset($node);
    }
    return $tree;
}

function render_nested_toc(array $tree) {
    if (empty($tree)) return '';
    $html = '<ul class="nested-toc-list">';
    foreach ($tree as $node) {
        $h = $node['heading'];
        $children = $node['children'];
        $html .= '<li class="toc-item level-' . $h['level'] . '">';
        
        if (!empty($children)) {
            $html .= '<details open class="toc-details">';
            $html .= '<summary class="toc-summary">';
            // El stopPropagation evita que al pulsar el enlace se cierre la carpeta
            $html .= '<a href="#' . htmlspecialchars($h['anchor']) . '" onclick="event.stopPropagation()">' . sa_safe_text($h['text']) . '</a>';
            $html .= '</summary>';
            $html .= render_nested_toc($children);
            $html .= '</details>';
        } else {
            $html .= '<div class="toc-link-wrapper">';
            $html .= '<a href="#' . htmlspecialchars($h['anchor']) . '">' . sa_safe_text($h['text']) . '</a>';
            $html .= '</div>';
        }
        
        $html .= '</li>';
    }
    $html .= '</ul>';
    return $html;
}

$nestedTocTree = build_nested_toc($headings);
$nestedTocHtml = render_nested_toc($nestedTocTree);
// ---------------------------------

$pageTitle = $note['title'] ?? 'Apunte';
require __DIR__ . '/includes/header.php';
?>

<?php if ($error): ?>
    <div class="alert"><?php echo sa_safe_text($error); ?></div>
    <p><a class="button-secondary" href="index.php">Volver al listado</a></p>
<?php else: ?>

    <!-- CORRECCIÓN: El bloque móvil va FUERA y ENCIMA de la cuadrícula principal -->
    <div class="mobile-only">
        <?php if (!empty($nestedTocTree)): ?>
            <details class="note-toc-details">
                <summary>Índice del documento</summary>
                <nav class="note-toc">
                    <?php echo $nestedTocHtml; ?>
                </nav>
            </details>
        <?php endif; ?>
    </div>

    <!-- Contenedor Grid estricto de 2 columnas -->
    <div class="note-layout">
        <aside class="note-sidebar">
            <a class="button-secondary" href="index.php">← Volver</a>

            <?php if (!empty($note['practice']['topics'])): ?>
                <div class="note-actions" style="margin: 1.2rem 0;">
                    <a
                        class="button-primary"
                        style="width: 100%; text-align: center; display: block;"
                        href="<?= htmlspecialchars(build_preparadortai_topic_practice_url(
                            $note['practice']['topics'],
                            [
                                'source' => 'studyassistant',
                                'note' => $note['id'] ?? '',
                                'processes' => $note['processes'] ?? [],
                                'profiles' => $note['profiles'] ?? [],
                            ]
                        )) ?>"
                    >
                        📝 Ponerme a prueba
                    </a>
                </div>
            <?php endif; ?>

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
                            <?php foreach ($note['processes'] as $process): ?>
                                <div><?php echo sa_safe_text($process); ?></div>
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
        </article>
    </div>
<?php endif; ?>

<?php require __DIR__ . '/includes/footer.php'; ?>