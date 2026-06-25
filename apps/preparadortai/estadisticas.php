<?php
include 'includes/header.php';

function fetch_single_row($link, $sql) {
    $result = mysqli_query($link, $sql);

    if (!$result) {
        return null;
    }

    return mysqli_fetch_assoc($result);
}

function fetch_all_rows($link, $sql) {
    $result = mysqli_query($link, $sql);

    if (!$result) {
        return [];
    }

    $rows = [];

    while ($row = mysqli_fetch_assoc($result)) {
        $rows[] = $row;
    }

    return $rows;
}

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function format_percentage($value) {
    if ($value === null || $value === '') {
        return '0,00%';
    }

    return number_format((float)$value, 2, ',', '.') . '%';
}

function format_decimal($value) {
    if ($value === null || $value === '') {
        return '-';
    }

    return number_format((float)$value, 2, ',', '.');
}

function is_ayto_madrid_aux_tic_category($category) {
    return strpos((string)$category, 'AYTO MADRID AUX TIC') === 0;
}

$globalStatsSql = "
    SELECT
      COUNT(*) AS total_answers,
      COALESCE(SUM(is_correct = 1), 0) AS correct_answers,
      COALESCE(SUM(is_correct = 0), 0) AS wrong_answers,
      CASE
        WHEN COUNT(*) = 0 THEN 0
        ELSE ROUND(SUM(is_correct = 1) * 100 / COUNT(*), 2)
      END AS accuracy_percentage
    FROM test_attempts
";

$categoryStatsSql = "
    SELECT
      categoria,
      COUNT(*) AS total_answers,
      COALESCE(SUM(is_correct = 1), 0) AS correct_answers,
      COALESCE(SUM(is_correct = 0), 0) AS wrong_answers,
      CASE
        WHEN COUNT(*) = 0 THEN 0
        ELSE ROUND(SUM(is_correct = 1) * 100 / COUNT(*), 2)
      END AS accuracy_percentage
    FROM test_attempts
    GROUP BY categoria
    ORDER BY accuracy_percentage ASC, total_answers DESC
";

$topicStatsSql = "
    SELECT
      bloque,
      tema,
      COUNT(*) AS total_answers,
      COALESCE(SUM(is_correct = 1), 0) AS correct_answers,
      COALESCE(SUM(is_correct = 0), 0) AS wrong_answers,
      CASE
        WHEN COUNT(*) = 0 THEN 0
        ELSE ROUND(SUM(is_correct = 1) * 100 / COUNT(*), 2)
      END AS accuracy_percentage
    FROM test_attempts
    GROUP BY bloque, tema
    ORDER BY accuracy_percentage ASC, total_answers DESC
";

$recentSessionsSql = "
    WITH question_counts AS (
        SELECT
            categoria,
            COUNT(*) AS total_questions
        FROM ptype
        GROUP BY categoria
    )
    SELECT
      ta.test_session_id,
      MIN(ta.created_at) AS started_at,
      MAX(ta.created_at) AS finished_at,
      MAX(ta.categoria) AS categoria,
      COALESCE(MAX(question_counts.total_questions), 0) AS total_questions,
      COUNT(*) AS total_answers,
      COALESCE(SUM(ta.is_correct = 1), 0) AS correct_answers,
      COALESCE(SUM(ta.is_correct = 0), 0) AS wrong_answers,
      CASE
        WHEN COUNT(*) = 0 THEN 0
        ELSE ROUND(SUM(ta.is_correct = 1) * 100 / COUNT(*), 2)
      END AS accuracy_percentage,
      CASE
        WHEN COALESCE(MAX(question_counts.total_questions), 0) = 0 THEN NULL
        ELSE ROUND(GREATEST(0, (COALESCE(SUM(ta.is_correct = 1), 0) - (COALESCE(SUM(ta.is_correct = 0), 0) / 3)) * 10 / MAX(question_counts.total_questions)), 2)
      END AS official_score
    FROM test_attempts ta
    LEFT JOIN question_counts
        ON question_counts.categoria = ta.categoria
    WHERE ta.test_session_id IS NOT NULL
    GROUP BY ta.test_session_id
    ORDER BY started_at DESC
    LIMIT 10
";

$globalStats = fetch_single_row($link, $globalStatsSql);
$categoryStats = fetch_all_rows($link, $categoryStatsSql);
$topicStats = fetch_all_rows($link, $topicStatsSql);
$recentSessions = fetch_all_rows($link, $recentSessionsSql);
$weakTopics = array_filter($topicStats, function ($row) {
    return (int)$row['total_answers'] >= 3;
});

$weakTopics = array_slice($weakTopics, 0, 10);

$totalAnswers = (int)($globalStats['total_answers'] ?? 0);
$correctAnswers = (int)($globalStats['correct_answers'] ?? 0);
$wrongAnswers = (int)($globalStats['wrong_answers'] ?? 0);
$accuracyPercentage = $globalStats['accuracy_percentage'] ?? 0;
$deletedAttempts = isset($_GET['deleted_attempts']) ? (int)$_GET['deleted_attempts'] : null;
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-chart-line"></i> Estadísticas
    </h2>
</div>

<?php if ($deletedAttempts !== null): ?>
    <div class="alert alert-success shadow-sm border-0">
        Se han borrado <?php echo $deletedAttempts; ?> respuestas registradas de la sesión seleccionada.
    </div>
<?php endif; ?>

<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Respuestas registradas</div>
                <div class="display-6 fw-bold text-dark"><?php echo $totalAnswers; ?></div>
            </div>
        </div>
    </div>

<div class="col-md-3">
    <div class="card shadow-sm border-0 h-100">
        <div class="card-body">
            <div class="text-secondary small text-uppercase fw-bold">Aciertos</div>
            <div class="display-6 fw-bold text-success"><?php echo $correctAnswers; ?></div>
        </div>
    </div>
</div>

<div class="col-md-3">
    <div class="card shadow-sm border-0 h-100">
        <div class="card-body">
            <div class="text-secondary small text-uppercase fw-bold">Fallos</div>
            <div class="display-6 fw-bold text-danger"><?php echo $wrongAnswers; ?></div>
        </div>
    </div>
</div>

<div class="col-md-3">
    <div class="card shadow-sm border-0 h-100">
        <div class="card-body">
            <div class="text-secondary small text-uppercase fw-bold">% acierto global</div>
            <div class="display-6 fw-bold text-primary"><?php echo format_percentage($accuracyPercentage); ?></div>
        </div>
    </div>
</div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-layer-group text-primary"></i> Rendimiento por categoría
        </h5>
    </div>

<div class="card-body">
    <?php if (empty($categoryStats)): ?>
        <p class="text-secondary mb-0">Todavía no hay respuestas registradas.</p>
    <?php else: ?>
        <div class="table-responsive">
            <table class="table table-hover align-middle">
                <thead>
                    <tr>
                        <th>Categoría</th>
                        <th class="text-end">Total</th>
                        <th class="text-end">Aciertos</th>
                        <th class="text-end">Fallos</th>
                        <th class="text-end">% acierto</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($categoryStats as $row): ?>
                        <tr>
                            <td><?php echo safe_text($row['categoria'] ?: 'Sin categoría'); ?></td>
                            <td class="text-end"><?php echo (int)$row['total_answers']; ?></td>
                            <td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td>
                            <td class="text-end text-danger"><?php echo (int)$row['wrong_answers']; ?></td>
                            <td class="text-end fw-bold"><?php echo format_percentage($row['accuracy_percentage']); ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php endif; ?>
</div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-book text-primary"></i> Rendimiento por bloque y tema
        </h5>
    </div>

<div class="card-body">
    <?php if (empty($topicStats)): ?>
        <p class="text-secondary mb-0">Todavía no hay respuestas registradas.</p>
    <?php else: ?>
        <div class="table-responsive">
            <table class="table table-hover align-middle">
                <thead>
                    <tr>
                        <th>Bloque</th>
                        <th>Tema</th>
                        <th class="text-end">Total</th>
                        <th class="text-end">Aciertos</th>
                        <th class="text-end">Fallos</th>
                        <th class="text-end">% acierto</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($topicStats as $row): ?>
                        <tr>
                            <td><?php echo safe_text($row['bloque'] ?? ''); ?></td>
                            <td><?php echo safe_text($row['tema'] ?? ''); ?></td>
                            <td class="text-end"><?php echo (int)$row['total_answers']; ?></td>
                            <td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td>
                            <td class="text-end text-danger"><?php echo (int)$row['wrong_answers']; ?></td>
                            <td class="text-end fw-bold"><?php echo format_percentage($row['accuracy_percentage']); ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php endif; ?>
</div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-clock-rotate-left text-primary"></i> Últimas sesiones de test
        </h5>
    </div>

<div class="card-body">
    <?php if (empty($recentSessions)): ?>
        <p class="text-secondary mb-0">
            Todavía no hay sesiones registradas.
        </p>
    <?php else: ?>
        <div class="table-responsive">
            <table class="table table-hover align-middle">
                <thead>
                    <tr>
                        <th>Fecha inicio</th>
                        <th>Categoría</th>
                        <th class="text-end">Contestadas</th>
                        <th class="text-end">En blanco</th>
                        <th class="text-end">Aciertos</th>
                        <th class="text-end">Fallos</th>
                        <th class="text-end">Resultado</th>
                        <th class="text-end">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($recentSessions as $row): ?>
                        <?php
                            $isOfficial = is_ayto_madrid_aux_tic_category($row['categoria']);
                            $totalQuestions = (int)$row['total_questions'];
                            $answered = (int)$row['total_answers'];
                            $blank = $isOfficial ? max(0, $totalQuestions - $answered) : null;
                        ?>
                        <tr>
                            <td><?php echo safe_text($row['started_at']); ?></td>
                            <td><?php echo safe_text($row['categoria'] ?: 'Sin categoría'); ?></td>
                            <td class="text-end"><?php echo $answered; ?></td>
                            <td class="text-end"><?php echo $isOfficial ? (int)$blank : '-'; ?></td>
                            <td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td>
                            <td class="text-end text-danger"><?php echo (int)$row['wrong_answers']; ?></td>
                            <td class="text-end fw-bold">
                                <?php echo $isOfficial ? format_decimal($row['official_score']) . ' / 10' : format_percentage($row['accuracy_percentage']); ?>
                            </td>
                            <td class="text-end">
                                <a href="detalle_sesion.php?session_id=<?php echo urlencode($row['test_session_id']); ?>" class="btn btn-outline-primary btn-sm">
                                    <i class="fa-solid fa-eye"></i> Ver detalle
                                </a>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php endif; ?>
</div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-bullseye text-primary"></i> Temas con menor porcentaje de acierto
        </h5>
    </div>

    <div class="card-body">
        <?php if (empty($weakTopics)): ?>
            <p class="text-secondary mb-0">
                Todavía no hay suficientes respuestas registradas para detectar temas a reforzar.
            </p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Bloque</th>
                            <th>Tema</th>
                            <th class="text-end">Total</th>
                            <th class="text-end">Aciertos</th>
                            <th class="text-end">Fallos</th>
                            <th class="text-end">% acierto</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($weakTopics as $row): ?>
                            <tr>
                                <td><?php echo safe_text($row['bloque'] ?? ''); ?></td>
                                <td><?php echo safe_text($row['tema'] ?? ''); ?></td>
                                <td class="text-end"><?php echo (int)$row['total_answers']; ?></td>
                                <td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td>
                                <td class="text-end text-danger fw-bold"><?php echo (int)$row['wrong_answers']; ?></td>
                                <td class="text-end fw-bold"><?php echo format_percentage($row['accuracy_percentage']); ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
