<?php
require_once __DIR__ . '/includes/knowledge.php';
require_once __DIR__ . '/includes/markdown.php';

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

$pageTitle = $note['title'] ?? 'Apunte';
require __DIR__ . '/includes/header.php';
?>

<?php if ($error): ?>
    <div class="alert"><?php echo sa_safe_text($error); ?></div>
    <p><a class="button-secondary" href="index.php">Volver al listado</a></p>
<?php else: ?>
    <div class="note-layout">
        <aside class="note-sidebar">
            <a class="button-secondary" href="index.php">← Volver</a>

            <?php if (!empty($topicQueries)): ?>
                <p style="margin:1rem 0;">
                    <a
                        class="button-primary"
                        href="../preparadortai/practica_tematica.php?<?=
                            http_build_query([
                                'topics' => $topicQueries,
                                'autosearch' => 1
                            ]);
                        ?>">
                        📝 Practicar este tema
                    </a>
                </p>
            <?php endif; ?>

            <h3>Metadatos</h3>

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

                <?php if (!empty($note['path'])): ?>
                    <dt>Fichero</dt>
                    <dd><code><?php echo sa_safe_text($note['path']); ?></code></dd>
                <?php endif; ?>
            </dl>
        </aside>

        <article class="note-content">
            <?php echo sa_render_markdown($markdown); ?>
        </article>
    </div>
<?php endif; ?>

<?php require __DIR__ . '/includes/footer.php'; ?>
