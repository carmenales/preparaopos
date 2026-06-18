<?php
include 'includes/header.php';

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
        return '-';
    }

    return number_format((float)$value, 2, ',', '.') . '%';
}

function get_status_badge($sessionCount, $maxAnswersInSession, $totalQuestions) {
    if ($sessionCount === 0) {
        return '<span class="badge bg-secondary">Pendiente</span>';
    }

    if ($totalQuestions > 0 && $maxAnswersInSession >= $totalQuestions) {
        return '<span class="badge bg-success">Completo</span>';
    }

    return '<span class="badge bg-warning text-dark">Parcial</span>';
}

$updatedQuestionSet = isset($_GET['updated_question_set']) ? (int)$_GET['updated_question_set'] : 0;

$filterOrganismo = isset($_GET['organismo']) ? trim($_GET['organismo']) : '';
$filterProceso = isset($_GET['proceso_selectivo']) ? trim($_GET['proceso_selectivo']) : '';
$filterYear = isset($_GET['year']) ? trim($_GET['year']) : '';
$filterTipo = isset($_GET['tipo']) ? trim($_GET['tipo']) : '';

$whereClauses = [];

if ($filterOrganismo !== '') {
    $whereClauses[] = "COALESCE(question_sets.organismo, '') = '" . mysqli_real_escape_string($link, $filterOrganismo) . "'";
}

if ($filterProceso !== '') {
    $whereClauses[] = "COALESCE(question_sets.proceso_selectivo, '') = '" . mysqli_real_escape_string($link, $filterProceso) . "'";
}

if ($filterYear !== '') {
    $whereClauses[] = "question_sets.convocatoria_year = " . (int)$filterYear;
}

if ($filterTipo !== '') {
    $whereClauses[] = "COALESCE(question_sets.tipo, '') = '" . mysqli_real_escape_string($link, $filterTipo) . "'";
}

$metadataFilterSql = empty($whereClauses) ? '' : 'WHERE ' . implode(' AND ', $whereClauses);

$organismos = fetch_all_rows($link, "
    SELECT DISTINCT organismo
    FROM question_sets
    WHERE organismo IS NOT NULL AND organismo <> ''
    ORDER BY organismo
");

$procesos = fetch_all_rows($link, "
    SELECT DISTINCT proceso_selectivo
    FROM question_sets
    WHERE proceso_selectivo IS NOT NULL AND proceso_selectivo <> ''
    ORDER BY proceso_selectivo
");

$years = fetch_all_rows($link, "
    SELECT DISTINCT convocatoria_year
    FROM question_sets
    WHERE convocatoria_year IS NOT NULL
    ORDER BY convocatoria_year DESC
");

$tipos = fetch_all_rows($link, "
    SELECT DISTINCT tipo
    FROM question_sets
    WHERE tipo IS NOT NULL AND tipo <> ''
    ORDER BY tipo
");

$progressSql = "
    WITH question_counts AS (
        SELECT
            categoria,
            COUNT(*) AS total_questions
        FROM ptype
        GROUP BY categoria
    ),
    session_stats AS (
        SELECT
            categoria,
            test_session_id,
            MIN(created_at) AS started_at,
            MAX(created_at) AS finished_at,
            COUNT(*) AS answered_questions,
            COALESCE(SUM(is_correct = 1), 0) AS correct_answers,
            COALESCE(SUM(is_correct = 0), 0) AS wrong_answers,
            CASE
                WHEN COUNT(*) = 0 THEN 0
                ELSE ROUND(SUM(is_correct = 1) * 100 / COUNT(*), 2)
            END AS accuracy_percentage
        FROM test_attempts
        WHERE test_session_id IS NOT NULL
        GROUP BY categoria, test_session_id
    ),
    category_progress AS (
        SELECT
            categoria,
            COUNT(*) AS session_count,
            MAX(answered_questions) AS max_answers_in_session,
            MAX(accuracy_percentage) AS best_accuracy_percentage
        FROM session_stats
        GROUP BY categoria
    ),
    last_sessions AS (
        SELECT *
        FROM (
            SELECT
                session_stats.*,
                ROW_NUMBER() OVER (
                    PARTITION BY categoria
                    ORDER BY started_at DESC, test_session_id DESC
                ) AS row_number
            FROM session_stats
        ) ranked_sessions
        WHERE row_number = 1
    )
    SELECT
        question_counts.categoria,
        question_counts.total_questions,
        question_sets.id AS question_set_id,
        question_sets.organismo,
        question_sets.proceso_selectivo,
        question_sets.convocatoria_year,
        question_sets.turno,
        question_sets.tipo,
        question_sets.descripcion,
        COALESCE(category_progress.session_count, 0) AS session_count,
        COALESCE(category_progress.max_answers_in_session, 0) AS max_answers_in_session,
        category_progress.best_accuracy_percentage,
        last_sessions.test_session_id AS last_session_id,
        last_sessions.started_at AS last_started_at,
        last_sessions.finished_at AS last_finished_at,
        last_sessions.answered_questions AS last_answered_questions,
        last_sessions.correct_answers AS last_correct_answers,
        last_sessions.wrong_answers AS last_wrong_answers,
        last_sessions.accuracy_percentage AS last_accuracy_percentage
    FROM question_counts
    LEFT JOIN question_sets
        ON question_sets.categoria = question_counts.categoria
    LEFT JOIN category_progress
        ON category_progress.categoria = question_counts.categoria
    LEFT JOIN last_sessions
        ON last_sessions.categoria = question_counts.categoria
    $metadataFilterSql
    ORDER BY
        CASE
            WHEN COALESCE(category_progress.session_count, 0) = 0 THEN 0
            ELSE 1
        END ASC,
        question_sets.organismo ASC,
        question_sets.proceso_selectivo ASC,
        question_sets.convocatoria_year DESC,
        question_counts.categoria ASC
";

$questionnaires = fetch_all_rows($link, $progressSql);

$totalQuestionnaires = count($questionnaires);
$pendingCount = 0;
$partialCount = 0;
$completedCount = 0;

foreach ($questionnaires as $row) {
    $sessionCount = (int)$row['session_count'];
    $maxAnswersInSession = (int)$row['max_answers_in_session'];
    $totalQuestions = (int)$row['total_questions'];

    if ($sessionCount === 0) {
        $pendingCount++;
    } elseif ($totalQuestions > 0 && $maxAnswersInSession >= $totalQuestions) {
        $completedCount++;
    } else {
        $partialCount++;
    }
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-clipboard-list"></i> Progreso de cuestionarios
    </h2>

    <a href="estadisticas.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-chart-line"></i> Estadísticas
    </a>
</div>

<?php if ($updatedQuestionSet === 1): ?>
    <div class="alert alert-success shadow-sm border-0">
        Metadatos del cuestionario actualizados correctamente.
    </div>
<?php endif; ?>

<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Cuestionarios</div>
                <div class="display-6 fw-bold text-dark"><?php echo $totalQuestionnaires; ?></div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Pendientes</div>
                <div class="display-6 fw-bold text-secondary"><?php echo $pendingCount; ?></div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Parciales</div>
                <div class="display-6 fw-bold text-warning"><?php echo $partialCount; ?></div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Completos</div>
                <div class="display-6 fw-bold text-success"><?php echo $completedCount; ?></div>
            </div>
        </div>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-filter text-primary"></i> Filtros
        </h5>
    </div>

    <div class="card-body">
        <form method="get" action="progreso_cuestionarios.php" class="row g-3 align-items-end">
            <div class="col-md-3">
                <label for="organismo" class="form-label">Organismo</label>
                <select id="organismo" name="organismo" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($organismos as $row): ?>
                        <option value="<?php echo safe_text($row['organismo']); ?>" <?php echo $filterOrganismo === $row['organismo'] ? 'selected' : ''; ?>>
                            <?php echo safe_text($row['organismo']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-3">
                <label for="proceso_selectivo" class="form-label">Proceso selectivo</label>
                <select id="proceso_selectivo" name="proceso_selectivo" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($procesos as $row): ?>
                        <option value="<?php echo safe_text($row['proceso_selectivo']); ?>" <?php echo $filterProceso === $row['proceso_selectivo'] ? 'selected' : ''; ?>>
                            <?php echo safe_text($row['proceso_selectivo']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2">
                <label for="year" class="form-label">Año</label>
                <select id="year" name="year" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($years as $row): ?>
                        <option value="<?php echo (int)$row['convocatoria_year']; ?>" <?php echo $filterYear === (string)$row['convocatoria_year'] ? 'selected' : ''; ?>>
                            <?php echo (int)$row['convocatoria_year']; ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2">
                <label for="tipo" class="form-label">Tipo</label>
                <select id="tipo" name="tipo" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($tipos as $row): ?>
                        <option value="<?php echo safe_text($row['tipo']); ?>" <?php echo $filterTipo === $row['tipo'] ? 'selected' : ''; ?>>
                            <?php echo safe_text($row['tipo']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2 d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    <i class="fa-solid fa-filter"></i> Filtrar
                </button>

                <a href="progreso_cuestionarios.php" class="btn btn-outline-secondary">
                    Limpiar
                </a>
            </div>
        </form>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-list-check text-primary"></i> Cuestionarios y tests disponibles
        </h5>
    </div>

    <div class="card-body">
        <?php if (empty($questionnaires)): ?>
            <p class="text-secondary mb-0">No hay cuestionarios disponibles con los filtros seleccionados.</p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Cuestionario / test</th>
                            <th>Organismo</th>
                            <th>Proceso selectivo</th>
                            <th class="text-end">Año</th>
                            <th>Turno</th>
                            <th>Tipo</th>
                            <th class="text-end">Preguntas</th>
                            <th class="text-end">Sesiones</th>
                            <th class="text-end">Estado</th>
                            <th class="text-end">Último resultado</th>
                            <th class="text-end">Mejor resultado</th>
                            <th class="text-end">Acciones</th>
                        </tr>
                    </thead>

                    <tbody>
                        <?php foreach ($questionnaires as $row): ?>
                            <?php
                                $categoria = $row['categoria'];
                                $totalQuestions = (int)$row['total_questions'];
                                $sessionCount = (int)$row['session_count'];
                                $maxAnswersInSession = (int)$row['max_answers_in_session'];
                                $lastSessionId = $row['last_session_id'];
                                $questionSetId = (int)$row['question_set_id'];

                                $testUrl = 'test.php?categoria=' . urlencode($categoria);
                                $detailUrl = $lastSessionId ? 'detalle_sesion.php?session_id=' . urlencode($lastSessionId) : null;
                                $editUrl = $questionSetId > 0 ? 'editar_cuestionario.php?id=' . $questionSetId : null;
                            ?>

                            <tr>
                                <td>
                                    <div class="fw-semibold"><?php echo safe_text($categoria); ?></div>
                                    <?php if (!empty($row['descripcion'])): ?>
                                        <div class="text-secondary small"><?php echo safe_text($row['descripcion']); ?></div>
                                    <?php endif; ?>
                                </td>

                                <td><?php echo safe_text($row['organismo'] ?: '-'); ?></td>
                                <td><?php echo safe_text($row['proceso_selectivo'] ?: '-'); ?></td>
                                <td class="text-end"><?php echo safe_text($row['convocatoria_year'] ?: '-'); ?></td>
                                <td><?php echo safe_text($row['turno'] ?: '-'); ?></td>
                                <td><?php echo safe_text($row['tipo'] ?: '-'); ?></td>

                                <td class="text-end"><?php echo $totalQuestions; ?></td>

                                <td class="text-end"><?php echo $sessionCount; ?></td>

                                <td class="text-end">
                                    <?php echo get_status_badge($sessionCount, $maxAnswersInSession, $totalQuestions); ?>
                                </td>

                                <td class="text-end">
                                    <?php if ($row['last_accuracy_percentage'] === null): ?>
                                        <span class="text-secondary">-</span>
                                    <?php else: ?>
                                        <div class="fw-bold"><?php echo format_percentage($row['last_accuracy_percentage']); ?></div>
                                        <div class="text-secondary small">
                                            <?php echo (int)$row['last_answered_questions']; ?> respondidas
                                        </div>
                                    <?php endif; ?>
                                </td>

                                <td class="text-end">
                                    <?php echo format_percentage($row['best_accuracy_percentage']); ?>
                                </td>

                                <td class="text-end">
                                    <div class="d-flex gap-2 justify-content-end">
                                        <a href="<?php echo safe_text($testUrl); ?>" class="btn btn-outline-primary btn-sm">
                                            <i class="fa-solid fa-play"></i> Hacer
                                        </a>

                                        <?php if ($detailUrl): ?>
                                            <a href="<?php echo safe_text($detailUrl); ?>" class="btn btn-outline-secondary btn-sm">
                                                <i class="fa-solid fa-eye"></i> Última sesión
                                            </a>
                                        <?php endif; ?>

                                        <?php if ($editUrl): ?>
                                            <a href="<?php echo safe_text($editUrl); ?>" class="btn btn-outline-dark btn-sm">
                                                <i class="fa-solid fa-pen"></i> Editar
                                            </a>
                                        <?php endif; ?>
                                    </div>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
