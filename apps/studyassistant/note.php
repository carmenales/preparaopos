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

$renderedContent = '';
if ($markdown !== null) {
    $renderedContent = sa_render_markdown($markdown);
    $renderedContent = add_heading_anchors($renderedContent);
}

$headings = $note['headings'] ?? [];

// Temas sugeridos para práctica (a partir de practice.topics, tags y official_topic)
$practiceTopics = sa_normalize_practice_topics($note);

// --- LÓGICA DE TOC ANIDADO ---
function build_nested_toc(array $headings) {
    $tree = [];
    $stack = [];

    foreach ($headings as $h) {
        if (($h['level'] ?? 0) < 2 || ($h['level'] ?? 0) > 4) {
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
// ---------------------------------

$pageTitle = $note['title'] ?? 'Apunte';
require __DIR__ . '/includes/header.php';
?>

<?php if ($error): ?>
    <div class="alert"><?php echo sa_safe_text($error); ?></div>
    <p><a class="button-secondary" href="index.php">Volver al listado</a></p>
<?php else: ?>

    <!-- Bloque móvil: índice encima de la cuadrícula principal -->
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

            <?php if (!empty($practiceTopics)): ?>
                <div class="note-practice-box" style="margin-top: 1.5rem;">
                    <h3 style="margin-top: 0; margin-bottom: 12px;">Temas para práctica</h3>

                    <form method="get" action="../preparadortai/practica_tematica.php">
                        <input type="hidden" name="source" value="studyassistant">
                        <input type="hidden" name="note" value="<?php echo sa_safe_text($note['id'] ?? ''); ?>">
                        <input type="hidden" name="autosearch" value="1">

                        <div class="practice-tags">
                            <?php foreach ($practiceTopics as $topic): ?>
                                <label class="practice-tag">
                                    <input type="checkbox" name="topics[]" value="<?php echo sa_safe_text($topic); ?>" checked>
                                    <span><?php echo sa_safe_text($topic); ?></span>
                                </label>
                            <?php endforeach; ?>
                        </div>

                        <div style="margin-top: 12px;">
                            <label for="practice-extra-topic" class="sr-only">Añadir tema</label>
                            <input
                                id="practice-extra-topic"
                                type="text"
                                class="practice-extra-input"
                                placeholder="Añadir otro tema"
                                maxlength="100"
                            >
                            <button type="button" class="button-secondary" id="add-practice-topic" style="margin-top: 8px;">
                                Añadir tema
                            </button>
                        </div>

                        <div class="note-actions" style="margin: 1.2rem 0;">
                            <button
                                type="submit"
                                class="button-primary"
                                style="width: 100%; text-align: center; display: block;"
                            >
                                📝 Ponerme a prueba
                            </button>
                        </div>
                    </form>
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
                    <dd><code><?php echo sa_safe_text($note['id'] ?? ''); ?></code></dd>

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

<script>
document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('practice-extra-topic');
    const button = document.getElementById('add-practice-topic');
    const form = button ? button.closest('form') : null;
    const box = form ? form.querySelector('.practice-tags') : null;

    if (!input || !button || !form || !box) return;

    button.addEventListener('click', function () {
        const value = input.value.trim();
        if (!value) return;

        const exists = Array.from(box.querySelectorAll('input[type="checkbox"]')).some(function (cb) {
            return cb.value.toLowerCase() === value.toLowerCase();
        });

        if (exists) {
            input.value = '';
            return;
        }

        const label = document.createElement('label');
        label.className = 'practice-tag';
        label.innerHTML = '<input type="checkbox" name="topics[]" value="' +
            value.replace(/"/g, '&quot;') +
            '" checked><span>' +
            value.replace(/</g, '&lt;').replace(/>/g, '&gt;') +
            '</span>';

        box.appendChild(label);
        input.value = '';
    });
});
</script>

<?php require __DIR__ . '/includes/footer.php'; ?>