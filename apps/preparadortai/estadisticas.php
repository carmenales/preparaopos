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


function format_signed_decimal($value, $suffix = '') {
    if ($value === null || $value === '') {
        return '-';
    }

    $floatValue = (float)$value;
    $prefix = $floatValue > 0 ? '+' : '';

    return $prefix . number_format($floatValue, 2, ',', '.') . $suffix;
}

function selected_attr($currentValue, $optionValue) {
    return (string)$currentValue === (string)$optionValue ? 'selected' : '';
}

function active_scope_class($currentScope, $scope) {
    return $currentScope === $scope ? 'btn-primary' : 'btn-outline-primary';
}

function build_query_string($overrides = []) {
    $params = $_GET;

    foreach ($overrides as $key => $value) {
        if ($value === null || $value === '') {
            unset($params[$key]);
        } else {
            $params[$key] = $value;
        }
    }

    return http_build_query($params);
}

function is_ayto_madrid_aux_tic_category($category) {
    return strpos((string)$category, 'AYTO MADRID AUX TIC') === 0;
}

function is_official_exam_row($row) {
    return ($row['tipo'] ?? '') === 'Examen oficial' || is_ayto_madrid_aux_tic_category($row['categoria'] ?? '');
}


function get_session_metric($row) {
    if (is_ayto_madrid_aux_tic_category($row['categoria'] ?? '') && $row['official_score'] !== null && $row['official_score'] !== '') {
        return [
            'type' => 'official',
            'value' => (float)$row['official_score'],
            'display' => format_decimal($row['official_score']) . ' / 10',
            'delta_suffix' => ' pts.'
        ];
    }

    return [
        'type' => 'percentage',
        'value' => (float)($row['accuracy_percentage'] ?? 0),
        'display' => format_percentage($row['accuracy_percentage'] ?? 0),
        'delta_suffix' => ' pp.'
    ];
}

function get_trend_badge($delta) {
    if ($delta === null) {
        return '<span class="badge bg-secondary">Sin comparación</span>';
    }

    if ($delta > 0.01) {
        return '<span class="badge bg-success">Mejora</span>';
    }

    if ($delta < -0.01) {
        return '<span class="badge bg-danger">Baja</span>';
    }

    return '<span class="badge bg-light text-dark">Igual</span>';
}

function get_priority_badge($row) {
    $total = (int)($row['total_answers'] ?? 0);
    $wrong = (int)($row['wrong_answers'] ?? 0);
    $accuracy = (float)($row['accuracy_percentage'] ?? 0);

    if (($total >= 10 && $accuracy < 60) || $wrong >= 10) {
        return '<span class="badge bg-danger">Alta</span>';
    }

    if (($total >= 5 && $accuracy < 75) || $wrong >= 5) {
        return '<span class="badge bg-warning text-dark">Media</span>';
    }

    return '<span class="badge bg-secondary">Baja</span>';
}

$filterOrganismo = isset($_GET['organismo']) ? trim($_GET['organismo']) : '';
$filterProceso = isset($_GET['proceso_selectivo']) ? trim($_GET['proceso_selectivo']) : '';
$filterYear = isset($_GET['year']) ? trim($_GET['year']) : '';
$filterTurno = isset($_GET['turno']) ? trim($_GET['turno']) : '';
$filterTipo = isset($_GET['tipo']) ? trim($_GET['tipo']) : '';
$filterCategoria = isset($_GET['categoria']) ? trim($_GET['categoria']) : '';
$scope = isset($_GET['scope']) ? trim($_GET['scope']) : 'all';

$allowedScopes = [
    '5' => 5,
    '10' => 10,
    '25' => 25,
    'all' => null,
];

if (!array_key_exists($scope, $allowedScopes)) {
    $scope = 'all';
}

$whereClauses = ["ta.test_session_id IS NOT NULL"];

if ($filterOrganismo !== '') {
    $whereClauses[] = "COALESCE(qs.organismo, '') = '" . mysqli_real_escape_string($link, $filterOrganismo) . "'";
}

if ($filterProceso !== '') {
    $whereClauses[] = "COALESCE(qs.proceso_selectivo, '') = '" . mysqli_real_escape_string($link, $filterProceso) . "'";
}

if ($filterYear !== '') {
    $whereClauses[] = "qs.convocatoria_year = " . (int)$filterYear;
}

if ($filterTurno !== '') {
    $whereClauses[] = "COALESCE(qs.turno, '') = '" . mysqli_real_escape_string($link, $filterTurno) . "'";
}

if ($filterTipo !== '') {
    $whereClauses[] = "COALESCE(qs.tipo, '') = '" . mysqli_real_escape_string($link, $filterTipo) . "'";
}

if ($filterCategoria !== '') {
    $whereClauses[] = "ta.categoria = '" . mysqli_real_escape_string($link, $filterCategoria) . "'";
}

$whereSql = 'WHERE ' . implode(' AND ', $whereClauses);
$limitSql = $allowedScopes[$scope] === null ? '' : 'LIMIT ' . (int)$allowedScopes[$scope];

$organismos = fetch_all_rows($link, "
    SELECT DISTINCT qs.organismo
    FROM test_attempts ta
    INNER JOIN question_sets qs ON qs.categoria = ta.categoria
    WHERE qs.organismo IS NOT NULL AND qs.organismo <> ''
    ORDER BY qs.organismo
");

$procesos = fetch_all_rows($link, "
    SELECT DISTINCT qs.proceso_selectivo
    FROM test_attempts ta
    INNER JOIN question_sets qs ON qs.categoria = ta.categoria
    WHERE qs.proceso_selectivo IS NOT NULL AND qs.proceso_selectivo <> ''
    ORDER BY qs.proceso_selectivo
");

$years = fetch_all_rows($link, "
    SELECT DISTINCT qs.convocatoria_year
    FROM test_attempts ta
    INNER JOIN question_sets qs ON qs.categoria = ta.categoria
    WHERE qs.convocatoria_year IS NOT NULL
    ORDER BY qs.convocatoria_year DESC
");

$turnos = fetch_all_rows($link, "
    SELECT DISTINCT qs.turno
    FROM test_attempts ta
    INNER JOIN question_sets qs ON qs.categoria = ta.categoria
    WHERE qs.turno IS NOT NULL AND qs.turno <> ''
    ORDER BY qs.turno
");

$tipos = fetch_all_rows($link, "
    SELECT DISTINCT qs.tipo
    FROM test_attempts ta
    INNER JOIN question_sets qs ON qs.categoria = ta.categoria
    WHERE qs.tipo IS NOT NULL AND qs.tipo <> ''
    ORDER BY qs.tipo
");

$categorias = fetch_all_rows($link, "
    SELECT DISTINCT ta.categoria
    FROM test_attempts ta
    WHERE ta.categoria IS NOT NULL AND ta.categoria <> ''
    ORDER BY ta.categoria
");

$sessionsSql = "
    WITH question_counts AS (
        SELECT
            categoria,
            COUNT(*) AS total_questions
        FROM ptype
        WHERE categoria IS NOT NULL AND categoria <> ''
        GROUP BY categoria
    ),
    session_stats AS (
        SELECT
            ta.test_session_id,
            MIN(ta.created_at) AS started_at,
            MAX(ta.created_at) AS finished_at,
            MAX(ta.categoria) AS categoria,
            MAX(qs.organismo) AS organismo,
            MAX(qs.proceso_selectivo) AS proceso_selectivo,
            MAX(qs.convocatoria_year) AS convocatoria_year,
            MAX(qs.turno) AS turno,
            MAX(qs.tipo) AS tipo,
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
        LEFT JOIN question_sets qs
            ON qs.categoria = ta.categoria
        LEFT JOIN question_counts
            ON question_counts.categoria = ta.categoria
        $whereSql
        GROUP BY ta.test_session_id
    )
    SELECT *
    FROM session_stats
    ORDER BY started_at DESC
    $limitSql
";

$sessions = fetch_all_rows($link, $sessionsSql);
$sessionIds = array_map(function ($row) {
    return $row['test_session_id'];
}, $sessions);

$quotedSessionIds = array_map(function ($sessionId) use ($link) {
    return "'" . mysqli_real_escape_string($link, (string)$sessionId) . "'";
}, $sessionIds);

$sessionFilterSql = empty($quotedSessionIds)
    ? "WHERE 1 = 0"
    : "WHERE ta.test_session_id IN (" . implode(',', $quotedSessionIds) . ")";

$globalStatsSql = "
    SELECT
        COUNT(*) AS total_answers,
        COALESCE(SUM(ta.is_correct = 1), 0) AS correct_answers,
        COALESCE(SUM(ta.is_correct = 0), 0) AS wrong_answers,
        CASE
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(ta.is_correct = 1) * 100 / COUNT(*), 2)
        END AS accuracy_percentage
    FROM test_attempts ta
    $sessionFilterSql
";

$categoryStatsSql = "
    SELECT
        ta.categoria,
        MAX(qs.organismo) AS organismo,
        MAX(qs.proceso_selectivo) AS proceso_selectivo,
        MAX(qs.convocatoria_year) AS convocatoria_year,
        MAX(qs.tipo) AS tipo,
        COUNT(DISTINCT ta.test_session_id) AS total_sessions,
        COUNT(*) AS total_answers,
        COALESCE(SUM(ta.is_correct = 1), 0) AS correct_answers,
        COALESCE(SUM(ta.is_correct = 0), 0) AS wrong_answers,
        CASE
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(ta.is_correct = 1) * 100 / COUNT(*), 2)
        END AS accuracy_percentage
    FROM test_attempts ta
    LEFT JOIN question_sets qs
        ON qs.categoria = ta.categoria
    $sessionFilterSql
    GROUP BY ta.categoria
    ORDER BY accuracy_percentage ASC, total_answers DESC
";

$blockStatsSql = "
    SELECT
        ta.bloque,
        COUNT(*) AS total_answers,
        COALESCE(SUM(ta.is_correct = 1), 0) AS correct_answers,
        COALESCE(SUM(ta.is_correct = 0), 0) AS wrong_answers,
        CASE
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(ta.is_correct = 1) * 100 / COUNT(*), 2)
        END AS accuracy_percentage
    FROM test_attempts ta
    $sessionFilterSql
    GROUP BY ta.bloque
    ORDER BY ta.bloque
";

$topicStatsSql = "
    SELECT
        ta.bloque,
        ta.tema,
        COUNT(*) AS total_answers,
        COALESCE(SUM(ta.is_correct = 1), 0) AS correct_answers,
        COALESCE(SUM(ta.is_correct = 0), 0) AS wrong_answers,
        CASE
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(ta.is_correct = 1) * 100 / COUNT(*), 2)
        END AS accuracy_percentage
    FROM test_attempts ta
    $sessionFilterSql
    GROUP BY ta.bloque, ta.tema
    ORDER BY accuracy_percentage ASC, total_answers DESC
";

$globalStats = fetch_single_row($link, $globalStatsSql);
$categoryStats = fetch_all_rows($link, $categoryStatsSql);
$blockStats = fetch_all_rows($link, $blockStatsSql);
$topicStats = fetch_all_rows($link, $topicStatsSql);

$weakTopics = [];

foreach ($topicStats as $row) {
    if ((int)$row['total_answers'] < 3) {
        continue;
    }

    $accuracy = (float)$row['accuracy_percentage'];
    $wrong = (int)$row['wrong_answers'];
    $row['priority_score'] = $wrong * max(0, 100 - $accuracy);
    $weakTopics[] = $row;
}

usort($weakTopics, function ($a, $b) {
    if ($a['priority_score'] === $b['priority_score']) {
        return (int)$b['wrong_answers'] <=> (int)$a['wrong_answers'];
    }

    return $a['priority_score'] < $b['priority_score'] ? 1 : -1;
});

$weakTopics = array_slice($weakTopics, 0, 10);

$totalAnswers = (int)($globalStats['total_answers'] ?? 0);
$correctAnswers = (int)($globalStats['correct_answers'] ?? 0);
$wrongAnswers = (int)($globalStats['wrong_answers'] ?? 0);
$accuracyPercentage = $globalStats['accuracy_percentage'] ?? 0;

$totalSessions = count($sessions);
$officialSessions = array_filter($sessions, function ($row) {
    return is_official_exam_row($row);
});

$aytoOfficialSessions = array_filter($sessions, function ($row) {
    return is_ayto_madrid_aux_tic_category($row['categoria'] ?? '');
});

$officialScores = array_values(array_filter(array_map(function ($row) {
    return $row['official_score'];
}, $aytoOfficialSessions), function ($value) {
    return $value !== null && $value !== '';
}));

$lastOfficialScore = !empty($officialScores) ? $officialScores[0] : null;
$bestOfficialScore = !empty($officialScores) ? max($officialScores) : null;
$avgOfficialScore = !empty($officialScores) ? array_sum($officialScores) / count($officialScores) : null;

$evolutionRows = [];
$previousMetric = null;
$chronologicalSessions = array_reverse($sessions);

foreach ($chronologicalSessions as $session) {
    $metric = get_session_metric($session);
    $delta = null;

    if ($previousMetric !== null && $previousMetric['type'] === $metric['type']) {
        $delta = $metric['value'] - $previousMetric['value'];
    }

    $evolutionRows[] = [
        'session' => $session,
        'metric' => $metric,
        'delta' => $delta,
    ];

    $previousMetric = $metric;
}

$officialExamRanking = [];

foreach ($aytoOfficialSessions as $session) {
    if ($session['official_score'] === null || $session['official_score'] === '') {
        continue;
    }

    $category = $session['categoria'];

    if (!isset($officialExamRanking[$category])) {
        $officialExamRanking[$category] = [
            'categoria' => $category,
            'organismo' => $session['organismo'],
            'proceso_selectivo' => $session['proceso_selectivo'],
            'convocatoria_year' => $session['convocatoria_year'],
            'turno' => $session['turno'],
            'attempts' => 0,
            'score_sum' => 0,
            'best_score' => null,
            'last_score' => $session['official_score'],
            'last_started_at' => $session['started_at'],
            'last_session_id' => $session['test_session_id'],
        ];
    }

    $score = (float)$session['official_score'];
    $officialExamRanking[$category]['attempts']++;
    $officialExamRanking[$category]['score_sum'] += $score;

    if ($officialExamRanking[$category]['best_score'] === null || $score > $officialExamRanking[$category]['best_score']) {
        $officialExamRanking[$category]['best_score'] = $score;
    }
}

$officialExamRanking = array_values($officialExamRanking);

foreach ($officialExamRanking as &$examRow) {
    $examRow['avg_score'] = $examRow['attempts'] > 0 ? $examRow['score_sum'] / $examRow['attempts'] : null;
}

unset($examRow);

usort($officialExamRanking, function ($a, $b) {
    if ($a['best_score'] === $b['best_score']) {
        return strcmp((string)$b['last_started_at'], (string)$a['last_started_at']);
    }

    return $a['best_score'] < $b['best_score'] ? 1 : -1;
});
$deletedAttempts = isset($_GET['deleted_attempts']) ? (int)$_GET['deleted_attempts'] : null;
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="text-primary fw-bold mb-1">
            <i class="fa-solid fa-chart-line"></i> Estadísticas
        </h2>
        <p class="text-secondary small mb-0">Análisis de rendimiento, evolución y áreas débiles.</p>
    </div>

    <div class="d-flex gap-2">
        <a href="progreso_cuestionarios.php" class="btn btn-outline-secondary">
            <i class="fa-solid fa-clipboard-list"></i> Progreso
        </a>
        <a href="historial_sesiones.php" class="btn btn-outline-primary">
            <i class="fa-solid fa-clock-rotate-left"></i> Historial
        </a>
    </div>
</div>

<?php if ($deletedAttempts !== null): ?>
    <div class="alert alert-success shadow-sm border-0">
        Se han borrado <?php echo $deletedAttempts; ?> respuestas registradas de la sesión seleccionada.
    </div>
<?php endif; ?>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-filter text-primary"></i> Filtros
        </h5>
    </div>

    <div class="card-body">
        <form method="get" action="estadisticas.php" class="row g-3 align-items-end">
            <input type="hidden" name="scope" value="<?php echo safe_text($scope); ?>">

            <div class="col-md-2">
                <label for="organismo" class="form-label">Organismo</label>
                <select id="organismo" name="organismo" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($organismos as $row): ?>
                        <option value="<?php echo safe_text($row['organismo']); ?>" <?php echo selected_attr($filterOrganismo, $row['organismo']); ?>>
                            <?php echo safe_text($row['organismo']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2">
                <label for="proceso_selectivo" class="form-label">Proceso</label>
                <select id="proceso_selectivo" name="proceso_selectivo" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($procesos as $row): ?>
                        <option value="<?php echo safe_text($row['proceso_selectivo']); ?>" <?php echo selected_attr($filterProceso, $row['proceso_selectivo']); ?>>
                            <?php echo safe_text($row['proceso_selectivo']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-1">
                <label for="year" class="form-label">Año</label>
                <select id="year" name="year" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($years as $row): ?>
                        <option value="<?php echo (int)$row['convocatoria_year']; ?>" <?php echo selected_attr($filterYear, $row['convocatoria_year']); ?>>
                            <?php echo (int)$row['convocatoria_year']; ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2">
                <label for="turno" class="form-label">Turno</label>
                <select id="turno" name="turno" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($turnos as $row): ?>
                        <option value="<?php echo safe_text($row['turno']); ?>" <?php echo selected_attr($filterTurno, $row['turno']); ?>>
                            <?php echo safe_text($row['turno']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2">
                <label for="tipo" class="form-label">Tipo</label>
                <select id="tipo" name="tipo" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($tipos as $row): ?>
                        <option value="<?php echo safe_text($row['tipo']); ?>" <?php echo selected_attr($filterTipo, $row['tipo']); ?>>
                            <?php echo safe_text($row['tipo']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2">
                <label for="categoria" class="form-label">Categoría</label>
                <select id="categoria" name="categoria" class="form-select">
                    <option value="">Todas</option>
                    <?php foreach ($categorias as $row): ?>
                        <option value="<?php echo safe_text($row['categoria']); ?>" <?php echo selected_attr($filterCategoria, $row['categoria']); ?>>
                            <?php echo safe_text($row['categoria']); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-1 d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    <i class="fa-solid fa-filter"></i>
                </button>

                <a href="estadisticas.php" class="btn btn-outline-secondary">
                    <i class="fa-solid fa-xmark"></i>
                </a>
            </div>
        </form>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-body">
        <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
            <div>
                <div class="text-secondary small text-uppercase fw-bold">Rango de análisis</div>
                <div class="fw-semibold">Sesiones incluidas: <?php echo $totalSessions; ?></div>
            </div>

            <div class="btn-group" role="group" aria-label="Rango de sesiones">
                <a href="estadisticas.php?<?php echo safe_text(build_query_string(['scope' => '5'])); ?>" class="btn <?php echo active_scope_class($scope, '5'); ?>">Últimas 5</a>
                <a href="estadisticas.php?<?php echo safe_text(build_query_string(['scope' => '10'])); ?>" class="btn <?php echo active_scope_class($scope, '10'); ?>">Últimas 10</a>
                <a href="estadisticas.php?<?php echo safe_text(build_query_string(['scope' => '25'])); ?>" class="btn <?php echo active_scope_class($scope, '25'); ?>">Últimas 25</a>
                <a href="estadisticas.php?<?php echo safe_text(build_query_string(['scope' => 'all'])); ?>" class="btn <?php echo active_scope_class($scope, 'all'); ?>">Todas</a>
            </div>
        </div>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">Sesiones</div><div class="display-6 fw-bold text-dark"><?php echo $totalSessions; ?></div></div></div></div>
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">Respuestas</div><div class="display-6 fw-bold text-dark"><?php echo $totalAnswers; ?></div></div></div></div>
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">Aciertos / Fallos</div><div class="display-6 fw-bold"><span class="text-success"><?php echo $correctAnswers; ?></span><span class="text-secondary">/</span><span class="text-danger"><?php echo $wrongAnswers; ?></span></div></div></div></div>
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">% acierto</div><div class="display-6 fw-bold text-primary"><?php echo format_percentage($accuracyPercentage); ?></div></div></div></div>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">Exámenes oficiales</div><div class="display-6 fw-bold text-dark"><?php echo count($officialSessions); ?></div><div class="text-secondary small">Sesiones de tipo examen oficial</div></div></div></div>
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">Última nota oficial</div><div class="display-6 fw-bold text-primary"><?php echo format_decimal($lastOfficialScore); ?></div><div class="text-secondary small">Solo AYTO Madrid Aux TIC</div></div></div></div>
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">Mejor nota oficial</div><div class="display-6 fw-bold text-success"><?php echo format_decimal($bestOfficialScore); ?></div><div class="text-secondary small">Sobre 10</div></div></div></div>
    <div class="col-md-3"><div class="card shadow-sm border-0 h-100"><div class="card-body"><div class="text-secondary small text-uppercase fw-bold">Media nota oficial</div><div class="display-6 fw-bold text-dark"><?php echo format_decimal($avgOfficialScore); ?></div><div class="text-secondary small">Sobre 10</div></div></div></div>
</div>


<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white"><h5 class="mb-0 fw-bold"><i class="fa-solid fa-arrow-trend-up text-primary"></i> Evolución de sesiones</h5></div>
    <div class="card-body">
        <?php if (empty($evolutionRows)): ?>
            <p class="text-secondary mb-0">No hay sesiones con los filtros seleccionados.</p>
        <?php else: ?>
            <div class="table-responsive"><table class="table table-hover align-middle"><thead><tr><th>Fecha</th><th>Categoría</th><th class="text-end">Resultado</th><th class="text-end">Variación</th><th class="text-end">Tendencia</th><th class="text-end">Acciones</th></tr></thead><tbody>
                <?php foreach ($evolutionRows as $row): ?>
                    <?php
                        $session = $row['session'];
                        $metric = $row['metric'];
                        $delta = $row['delta'];
                        $deltaClass = $delta === null ? 'text-secondary' : ($delta >= 0 ? 'text-success' : 'text-danger');
                        $detailUrl = 'detalle_sesion.php?session_id=' . urlencode($session['test_session_id']);
                    ?>
                    <tr>
                        <td><?php echo safe_text($session['started_at']); ?></td>
                        <td><div class="fw-semibold"><?php echo safe_text($session['categoria'] ?: 'Sin categoría'); ?></div><?php if (!empty($session['tipo'])): ?><div class="text-secondary small"><?php echo safe_text($session['tipo']); ?></div><?php endif; ?></td>
                        <td class="text-end fw-bold"><?php echo safe_text($metric['display']); ?></td>
                        <td class="text-end fw-bold <?php echo $deltaClass; ?>"><?php echo $delta === null ? '-' : format_signed_decimal($delta, $metric['delta_suffix']); ?></td>
                        <td class="text-end"><?php echo get_trend_badge($delta); ?></td>
                        <td class="text-end"><a href="<?php echo safe_text($detailUrl); ?>" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-eye"></i> Detalle</a></td>
                    </tr>
                <?php endforeach; ?>
            </tbody></table></div>
            <p class="text-secondary small mb-0">La variación solo se calcula cuando la sesión anterior usa la misma escala: nota oficial sobre 10 o porcentaje.</p>
        <?php endif; ?>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white"><h5 class="mb-0 fw-bold"><i class="fa-solid fa-file-signature text-primary"></i> Ranking de exámenes oficiales</h5></div>
    <div class="card-body">
        <?php if (empty($officialExamRanking)): ?>
            <p class="text-secondary mb-0">Todavía no hay exámenes oficiales con nota calculable.</p>
        <?php else: ?>
            <div class="table-responsive"><table class="table table-hover align-middle"><thead><tr><th>Examen</th><th class="text-end">Intentos</th><th class="text-end">Última nota</th><th class="text-end">Mejor nota</th><th class="text-end">Media</th><th class="text-end">Última fecha</th><th class="text-end">Acciones</th></tr></thead><tbody>
                <?php foreach ($officialExamRanking as $row): ?>
                    <?php
                        $detailUrl = 'detalle_sesion.php?session_id=' . urlencode($row['last_session_id']);
                        $repeatUrl = 'test.php?categoria=' . urlencode($row['categoria']);
                    ?>
                    <tr>
                        <td><div class="fw-semibold"><?php echo safe_text($row['categoria']); ?></div><div class="text-secondary small"><?php echo safe_text(trim(($row['organismo'] ?? '') . ' · ' . ($row['proceso_selectivo'] ?? '') . ' · ' . ($row['convocatoria_year'] ?? '') . ' · ' . ($row['turno'] ?? ''), ' ·')); ?></div></td>
                        <td class="text-end"><?php echo (int)$row['attempts']; ?></td>
                        <td class="text-end fw-bold text-primary"><?php echo format_decimal($row['last_score']); ?> / 10</td>
                        <td class="text-end fw-bold text-success"><?php echo format_decimal($row['best_score']); ?> / 10</td>
                        <td class="text-end fw-bold"><?php echo format_decimal($row['avg_score']); ?> / 10</td>
                        <td class="text-end"><?php echo safe_text($row['last_started_at']); ?></td>
                        <td class="text-end"><div class="d-flex gap-2 justify-content-end"><a href="<?php echo safe_text($detailUrl); ?>" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-eye"></i> Detalle</a><a href="<?php echo safe_text($repeatUrl); ?>" class="btn btn-outline-secondary btn-sm"><i class="fa-solid fa-rotate-right"></i> Repetir</a></div></td>
                    </tr>
                <?php endforeach; ?>
            </tbody></table></div>
        <?php endif; ?>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white"><h5 class="mb-0 fw-bold"><i class="fa-solid fa-layer-group text-primary"></i> Rendimiento por categoría</h5></div>
    <div class="card-body">
        <?php if (empty($categoryStats)): ?>
            <p class="text-secondary mb-0">No hay datos con los filtros seleccionados.</p>
        <?php else: ?>
            <div class="table-responsive"><table class="table table-hover align-middle"><thead><tr><th>Categoría</th><th>Tipo</th><th class="text-end">Sesiones</th><th class="text-end">Total</th><th class="text-end">Aciertos</th><th class="text-end">Fallos</th><th class="text-end">% acierto</th><th style="width: 180px;">Progreso</th></tr></thead><tbody>
                <?php foreach ($categoryStats as $row): ?>
                    <tr>
                        <td><div class="fw-semibold"><?php echo safe_text($row['categoria'] ?: 'Sin categoría'); ?></div><?php if (!empty($row['organismo']) || !empty($row['proceso_selectivo']) || !empty($row['convocatoria_year'])): ?><div class="text-secondary small"><?php echo safe_text(trim(($row['organismo'] ?? '') . ' · ' . ($row['proceso_selectivo'] ?? '') . ' · ' . ($row['convocatoria_year'] ?? ''), ' ·')); ?></div><?php endif; ?></td>
                        <td><?php echo safe_text($row['tipo'] ?: '-'); ?></td><td class="text-end"><?php echo (int)$row['total_sessions']; ?></td><td class="text-end"><?php echo (int)$row['total_answers']; ?></td><td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td><td class="text-end text-danger"><?php echo (int)$row['wrong_answers']; ?></td><td class="text-end fw-bold"><?php echo format_percentage($row['accuracy_percentage']); ?></td>
                        <td><div class="progress" style="height: 8px;"><div class="progress-bar" role="progressbar" style="width: <?php echo (float)$row['accuracy_percentage']; ?>%;" aria-valuenow="<?php echo (float)$row['accuracy_percentage']; ?>" aria-valuemin="0" aria-valuemax="100"></div></div></td>
                    </tr>
                <?php endforeach; ?>
            </tbody></table></div>
        <?php endif; ?>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white"><h5 class="mb-0 fw-bold"><i class="fa-solid fa-chart-column text-primary"></i> Resultados por bloque</h5></div>
    <div class="card-body">
        <?php if (empty($blockStats)): ?>
            <p class="text-secondary mb-0">No hay datos con los filtros seleccionados.</p>
        <?php else: ?>
            <div class="row g-3">
                <?php foreach ($blockStats as $row): ?>
                    <div class="col-md-3"><div class="border rounded p-3 bg-white h-100"><div class="fw-bold mb-1"><?php echo safe_text($row['bloque'] ?: 'Sin bloque'); ?></div><div class="small text-secondary mb-2"><?php echo (int)$row['total_answers']; ?> respuestas · <?php echo (int)$row['wrong_answers']; ?> fallos</div><div class="d-flex justify-content-between small mb-1"><span>% acierto</span><strong><?php echo format_percentage($row['accuracy_percentage']); ?></strong></div><div class="progress" style="height: 8px;"><div class="progress-bar" role="progressbar" style="width: <?php echo (float)$row['accuracy_percentage']; ?>%;" aria-valuenow="<?php echo (float)$row['accuracy_percentage']; ?>" aria-valuemin="0" aria-valuemax="100"></div></div></div></div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white"><h5 class="mb-0 fw-bold"><i class="fa-solid fa-book text-primary"></i> Rendimiento por bloque y tema</h5></div>
    <div class="card-body">
        <?php if (empty($topicStats)): ?>
            <p class="text-secondary mb-0">No hay datos con los filtros seleccionados.</p>
        <?php else: ?>
            <div class="table-responsive"><table class="table table-hover align-middle"><thead><tr><th>Bloque</th><th>Tema</th><th class="text-end">Total</th><th class="text-end">Aciertos</th><th class="text-end">Fallos</th><th class="text-end">% acierto</th></tr></thead><tbody>
                <?php foreach ($topicStats as $row): ?>
                    <tr><td><?php echo safe_text($row['bloque'] ?? ''); ?></td><td><?php echo safe_text($row['tema'] ?? ''); ?></td><td class="text-end"><?php echo (int)$row['total_answers']; ?></td><td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td><td class="text-end text-danger"><?php echo (int)$row['wrong_answers']; ?></td><td class="text-end fw-bold"><?php echo format_percentage($row['accuracy_percentage']); ?></td></tr>
                <?php endforeach; ?>
            </tbody></table></div>
        <?php endif; ?>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white"><h5 class="mb-0 fw-bold"><i class="fa-solid fa-bullseye text-primary"></i> Diagnóstico de áreas débiles</h5></div>
    <div class="card-body">
        <?php if (empty($weakTopics)): ?>
            <p class="text-secondary mb-0">Todavía no hay suficientes respuestas registradas para detectar temas a reforzar.</p>
        <?php else: ?>
            <div class="table-responsive"><table class="table table-hover align-middle"><thead><tr><th>Bloque</th><th>Tema</th><th class="text-end">Prioridad</th><th class="text-end">Total</th><th class="text-end">Aciertos</th><th class="text-end">Fallos</th><th class="text-end">% acierto</th><th class="text-end">Indicador</th></tr></thead><tbody>
                <?php foreach ($weakTopics as $row): ?>
                    <tr><td><?php echo safe_text($row['bloque'] ?? ''); ?></td><td><?php echo safe_text($row['tema'] ?? ''); ?></td><td class="text-end"><?php echo get_priority_badge($row); ?></td><td class="text-end"><?php echo (int)$row['total_answers']; ?></td><td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td><td class="text-end text-danger fw-bold"><?php echo (int)$row['wrong_answers']; ?></td><td class="text-end fw-bold"><?php echo format_percentage($row['accuracy_percentage']); ?></td><td class="text-end text-secondary small"><?php echo format_decimal($row['priority_score']); ?></td></tr>
                <?php endforeach; ?>
            </tbody></table></div>
            <p class="text-secondary small mb-0">El indicador prioriza temas con más fallos y menor porcentaje de acierto. Se ignoran temas con menos de 3 respuestas.</p>
        <?php endif; ?>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
