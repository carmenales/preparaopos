<?php
include 'includes/header.php';
require_once __DIR__ . '/includes/question_search.php';

$query = trim((string)($_GET['q'] ?? ''));
$category = trim((string)($_GET['categoria'] ?? ''));
$block = trim((string)($_GET['bloque'] ?? ''));
$topic = trim((string)($_GET['tema'] ?? ''));
$error = trim((string)($_GET['error'] ?? ''));

$hasFilters = $query !== '' || $category !== '' || $block !== '' || $topic !== '';
$categories = topic_search_categories($link);
$results = [];
$searchError = null;

if ($hasFilters) {
    try {
        $results = topic_search_questions($link, [
            'q' => $query,
            'categoria' => $category,
            'bloque' => $block,
            'tema' => $topic,
        ]);
    } catch (RuntimeException $exception) {
        $searchError = $exception->getMessage();
    }
}

$defaultQuestionCount = min(20, max(1, count($results)));
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1">
            <i class="fa-solid fa-magnifying-glass-chart"></i> Práctica temática
        </h2>
        <p class="text-secondary small mb-0">
            Busca preguntas relacionadas con un tema y genera un test con los resultados seleccionados.
        </p>
    </div>
</div>

<?php if ($error !== ''): ?>
    <div class="alert alert-danger shadow-sm border-0">
        <?php echo topic_search_safe_text($error); ?>
    </div>
<?php endif; ?>

<?php if ($searchError !== null): ?>
    <div class="alert alert-danger shadow-sm border-0">
        <?php echo topic_search_safe_text($searchError); ?>
    </div>
<?php endif; ?>

<div class="card border-0 shadow-sm mb-4">
    <div class="card-body">
        <form method="get" action="practica_tematica.php">
            <div class="row g-3 align-items-end">
                <div class="col-lg-5">
                    <label for="q" class="form-label small fw-bold">Palabras o frases</label>
                    <input
                        type="text"
                        id="q"
                        name="q"
                        class="form-control"
                        value="<?php echo topic_search_safe_text($query); ?>"
                        placeholder='Ej. oracle backup, tcp ip, "modelo OSI"'
                        maxlength="200"
                    >
                    <div class="form-text">Todas las palabras deben aparecer en el contenido de la pregunta.</div>
                </div>

                <div class="col-lg-3">
                    <label for="categoria" class="form-label small fw-bold">Categoría</label>
                    <select id="categoria" name="categoria" class="form-select">
                        <option value="">Todas</option>
                        <?php foreach ($categories as $item): ?>
                            <option value="<?php echo topic_search_safe_text($item); ?>" <?php echo $category === $item ? 'selected' : ''; ?>>
                                <?php echo topic_search_safe_text($item); ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div class="col-lg-1 col-md-3">
                    <label for="bloque" class="form-label small fw-bold">Bloque</label>
                    <input type="number" id="bloque" name="bloque" class="form-control" min="0" value="<?php echo topic_search_safe_text($block); ?>">
                </div>

                <div class="col-lg-1 col-md-3">
                    <label for="tema" class="form-label small fw-bold">Tema</label>
                    <input type="number" id="tema" name="tema" class="form-control" min="0" value="<?php echo topic_search_safe_text($topic); ?>">
                </div>

                <div class="col-lg-2 d-grid">
                    <button type="submit" class="btn btn-primary">
                        <i class="fa-solid fa-magnifying-glass"></i> Buscar
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>

<?php if (!$hasFilters): ?>
    <div class="alert alert-info shadow-sm border-0">
        Prueba búsquedas como <strong>oracle backup</strong>, <strong>soc siem</strong>,
        <strong>san nas das</strong> o <strong>protección de datos</strong>.
    </div>
<?php elseif ($searchError === null && empty($results)): ?>
    <div class="alert alert-warning shadow-sm border-0">
        No se han encontrado preguntas con los criterios indicados.
    </div>
<?php elseif ($searchError === null): ?>
    <form method="post" action="logic/start_topic_test.php" id="topic-test-form">
        <input type="hidden" name="q" value="<?php echo topic_search_safe_text($query); ?>">

        <div class="card border-0 shadow-sm mb-3">
            <div class="card-body">
                <div class="row g-3 align-items-end">
                    <div class="col-lg-4">
                        <div class="fw-bold">
                            <?php echo count($results); ?> preguntas encontradas
                        </div>
                        <div class="text-secondary small">Selecciona las que quieras incluir en la práctica.</div>
                    </div>

                    <div class="col-lg-3">
                        <label for="max_questions" class="form-label small fw-bold">Número máximo</label>
                        <input
                            type="number"
                            id="max_questions"
                            name="max_questions"
                            class="form-control"
                            min="1"
                            max="100"
                            value="<?php echo (int)$defaultQuestionCount; ?>"
                            required
                        >
                    </div>

                    <div class="col-lg-3">
                        <label for="correccion" class="form-label small fw-bold">Corrección</label>
                        <select id="correccion" name="correccion" class="form-select">
                            <option value="inmediata">Al responder</option>
                            <option value="final">Al final</option>
                        </select>
                    </div>

                    <div class="col-lg-2 d-grid">
                        <button type="submit" class="btn btn-success">
                            <i class="fa-solid fa-play"></i> Generar test
                        </button>
                    </div>
                </div>

                <hr>

                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="select-all" checked>
                    <label class="form-check-label fw-bold" for="select-all">
                        Seleccionar todas
                    </label>
                </div>
            </div>
        </div>

        <div class="row g-3">
            <?php foreach ($results as $row): ?>
                <div class="col-12">
                    <label class="card border-0 shadow-sm h-100 topic-result-card" for="question-<?php echo (int)$row['id']; ?>">
                        <div class="card-body d-flex gap-3 align-items-start">
                            <input
                                class="form-check-input mt-1 topic-question-checkbox"
                                type="checkbox"
                                name="question_ids[]"
                                value="<?php echo (int)$row['id']; ?>"
                                id="question-<?php echo (int)$row['id']; ?>"
                                checked
                            >

                            <div class="flex-grow-1">
                                <div class="d-flex flex-wrap gap-2 mb-2">
                                    <span class="badge bg-primary"><?php echo topic_search_safe_text($row['categoria']); ?></span>

                                    <?php if ($row['bloque'] !== null && $row['bloque'] !== ''): ?>
                                        <span class="badge bg-light text-dark border">Bloque <?php echo (int)$row['bloque']; ?></span>
                                    <?php endif; ?>

                                    <?php if ($row['tema'] !== null && $row['tema'] !== ''): ?>
                                        <span class="badge bg-light text-dark border">Tema <?php echo (int)$row['tema']; ?></span>
                                    <?php endif; ?>

                                    <span class="badge bg-secondary">#<?php echo (int)$row['id']; ?></span>
                                </div>

                                <div class="text-dark">
                                    <?php echo topic_search_safe_text(topic_search_truncate($row['pregunta'])); ?>
                                </div>
                            </div>
                        </div>
                    </label>
                </div>
            <?php endforeach; ?>
        </div>
    </form>
<?php endif; ?>

<script>
(function () {
    const selectAll = document.getElementById('select-all');
    const checkboxes = Array.from(document.querySelectorAll('.topic-question-checkbox'));
    const form = document.getElementById('topic-test-form');
    const maxQuestions = document.getElementById('max_questions');

    function selectedCount() {
        return checkboxes.filter(function (checkbox) {
            return checkbox.checked;
        }).length;
    }

    function updateControls() {
        if (!selectAll || !maxQuestions) return;

        const selected = selectedCount();
        selectAll.checked = selected === checkboxes.length && checkboxes.length > 0;
        selectAll.indeterminate = selected > 0 && selected < checkboxes.length;
        maxQuestions.max = Math.max(1, Math.min(100, selected));

        if (selected > 0 && parseInt(maxQuestions.value, 10) > selected) {
            maxQuestions.value = Math.min(20, selected);
        }
    }

    if (selectAll) {
        selectAll.addEventListener('change', function () {
            checkboxes.forEach(function (checkbox) {
                checkbox.checked = selectAll.checked;
            });
            updateControls();
        });
    }

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', updateControls);
    });

    if (form) {
        form.addEventListener('submit', function (event) {
            if (selectedCount() === 0) {
                event.preventDefault();
                window.alert('Selecciona al menos una pregunta.');
            }
        });
    }

    updateControls();
})();
</script>

<?php include 'includes/footer.php'; ?>
