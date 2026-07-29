<?php
require_once __DIR__ . '/includes/knowledge.php';

$notes = sa_load_index();
$query = isset($_GET['q']) ? trim($_GET['q']) : '';
$tag = isset($_GET['tag']) ? trim($_GET['tag']) : '';
$process = isset($_GET['process']) ? trim($_GET['process']) : '';
$status = isset($_GET['status']) ? trim($_GET['status']) : '';

$tags = sa_collect_unique($notes, 'tags');
$processes = sa_collect_unique($notes, 'processes');
$statuses = sa_collect_statuses($notes);
$filteredNotes = sa_filter_notes($notes, $query, $tag, $process, $status);

$pageTitle = 'Study Assistant';
require __DIR__ . '/includes/header.php';
?>

<section class="hero">
    <h1>Apuntes</h1>
    <p>Consulta, filtra y busca en la base de conocimiento Markdown.</p>
</section>

<?php if (empty($notes)): ?>
    <div class="alert">
        No hay índice generado todavía. Ejecuta:
        <code>python scripts/build_knowledge_index.py</code>
    </div>
<?php endif; ?>

<form class="filters" method="get" action="index.php">
    <div class="field field-wide">
        <label for="q">Buscar</label>
        <input id="q" name="q" type="search" value="<?php echo sa_safe_text($query); ?>" placeholder="tokenización, MLOps, ENS...">
    </div>

    <div class="field">
        <label for="tag">Etiqueta</label>
        <select id="tag" name="tag">
            <option value="">Todas</option>
            <?php foreach ($tags as $item): ?>
                <option value="<?php echo sa_safe_text($item); ?>" <?php echo sa_selected_attr($tag, $item); ?>>
                    <?php echo sa_safe_text($item); ?>
                </option>
            <?php endforeach; ?>
        </select>
    </div>

    <div class="field">
        <label for="process">Proceso</label>
        <select id="process" name="process">
            <option value="">Todos</option>
            <?php foreach ($processes as $item): ?>
                <option value="<?php echo sa_safe_text($item); ?>" <?php echo sa_selected_attr($process, $item); ?>>
                    <?php echo sa_safe_text($item); ?>
                </option>
            <?php endforeach; ?>
        </select>
    </div>

    <div class="field">
        <label for="status">Estado</label>
        <select id="status" name="status">
            <option value="">Todos</option>
            <?php foreach ($statuses as $item): ?>
                <option value="<?php echo sa_safe_text($item); ?>" <?php echo sa_selected_attr($status, $item); ?>>
                    <?php echo sa_safe_text($item); ?>
                </option>
            <?php endforeach; ?>
        </select>
    </div>

    <div class="actions">
        <button type="submit">Filtrar</button>
        <a class="button-secondary" href="index.php">Limpiar</a>
    </div>
</form>

<div class="summary">
    <strong><?php echo count($filteredNotes); ?></strong> apuntes mostrados de <?php echo count($notes); ?> indexados.
</div>

<section class="semantic-search">
    <h2>Búsqueda semántica</h2>
    <p class="meta">Busca por significado dentro del contenido de los apuntes, no solo por título o etiquetas.</p>

    <div class="field field-wide">
        <label for="semantic-q">Pregunta o concepto</label>
        <input id="semantic-q" type="search" placeholder="ej. diferencia entre autenticación y autorización">
        <button id="semantic-search-btn" type="button">Buscar</button>
    </div>

    <div id="semantic-search-status" class="semantic-search-status" hidden></div>
    <ul id="semantic-search-results" class="semantic-results"></ul>
</section>

<script src="assets/semantic-search.js"></script>

<section class="note-grid">
    <?php foreach ($filteredNotes as $note): ?>
        <article class="note-card">
            <div class="note-card-header">
                <h2>
                    <a href="note.php?id=<?php echo urlencode($note['id']); ?>">
                        <?php echo sa_safe_text($note['title']); ?>
                    </a>
                </h2>
                <?php if (!empty($note['status'])): ?>
                    <span class="badge"><?php echo sa_safe_text($note['status']); ?></span>
                <?php endif; ?>
            </div>

            <?php if (!empty($note['official_topic'])): ?>
                <p class="meta"><?php echo sa_safe_text($note['official_topic']); ?></p>
            <?php endif; ?>

            <?php if (!empty($note['excerpt'])): ?>
                <p><?php echo sa_safe_text($note['excerpt']); ?></p>
            <?php endif; ?>

            <?php if (!empty($note['tags'])): ?>
                <div class="tags">
                    <?php foreach ($note['tags'] as $noteTag): ?>
                        <a class="tag" href="index.php?tag=<?php echo urlencode($noteTag); ?>">
                            <?php echo sa_safe_text($noteTag); ?>
                        </a>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
        </article>
    <?php endforeach; ?>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
