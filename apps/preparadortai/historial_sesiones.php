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

function format_score_scale($value) {
    if ($value === null || $value === '') {
        return '10';
    }

    $floatValue = (float)$value;

    if (abs($floatValue - round($floatValue)) < 0.0001) {
        return (string)(int)round($floatValue);
    }

    return format_decimal($floatValue);
}

function is_official_exam_row($row) {
    return ($row['tipo'] ?? '') === 'Examen oficial';
}

function has_official_scoring($row) {
    return is_official_exam_row($row)
        && ($row['scoring_rule_code'] ?? '') !== ''
        && ($row['official_score'] ?? null) !== null
        && ($row['official_score'] ?? '') !== '';
}

function selected_attr($currentValue, $optionValue) {
    return (string)$currentValue === (string)$optionValue ? 'selected' : '';
}

$filterOrganismo = isset($_GET['organismo']) ? trim($_GET['organismo']) : '';
$filterProceso = isset($_GET['proceso_selectivo']) ? trim($_GET['proceso_selectivo']) : '';
$filterYear = isset($_GET['year']) ? trim($_GET['year']) : '';
$filterTurno = isset($_GET['turno']) ? trim($_GET['turno']) : '';
$filterTipo = isset($_GET['tipo']) ? trim($_GET['tipo']) : '';
$filterCategoria = isset($_GET['categoria']) ? trim($_GET['categoria']) : '';

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
            MAX(sr.code) AS scoring_rule_code,
            MAX(sr.name) AS scoring_rule_name,
            MAX(sr.correct_score) AS correct_score,
            MAX(sr.wrong_penalty) AS wrong_penalty,
            COALESCE(MAX(sr.blank_score), 0) AS blank_score,
            COALESCE(MAX(sr.score_scale), 10) AS score_scale,
            COALESCE(MAX(sr.min_score_zero), 1) AS min_score_zero,
            COALESCE(MAX(question_counts.total_questions), 0) AS total_questions,
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
        LEFT JOIN scoring_rules sr
            ON sr.id = qs.scoring_rule_id
        LEFT JOIN question_counts
            ON question_counts.categoria = ta.categoria
        $whereSql
        GROUP BY ta.test_session_id
    ),
    session_scores AS (
        SELECT
            session_stats.*,
            GREATEST(0, total_questions - total_answers) AS blank_answers,
            (
                (correct_answers * COALESCE(correct_score, 0))
                - (wrong_answers * COALESCE(wrong_penalty, 0))
                + (GREATEST(0, total_questions - total_answers) * COALESCE(blank_score, 0))
            ) AS raw_official_direct_score
        FROM session_stats
    )
    SELECT
        session_scores.*,
        CASE
            WHEN tipo = 'Examen oficial'
                AND scoring_rule_code IS NOT NULL
                AND correct_score IS NOT NULL
                AND wrong_penalty IS NOT NULL
                AND total_questions > 0
                AND correct_score > 0
            THEN ROUND(
                CASE
                    WHEN min_score_zero = 1 THEN GREATEST(0, raw_official_direct_score)
                    ELSE raw_official_direct_score
                END,
                2
            )
            ELSE NULL
        END AS official_direct_score,
        CASE
            WHEN tipo = 'Examen oficial'
                AND scoring_rule_code IS NOT NULL
                AND correct_score IS NOT NULL
                AND wrong_penalty IS NOT NULL
                AND total_questions > 0
                AND correct_score > 0
            THEN ROUND(
                (
                    CASE
                        WHEN min_score_zero = 1 THEN GREATEST(0, raw_official_direct_score)
                        ELSE raw_official_direct_score
                    END
                ) * score_scale / (total_questions * correct_score),
                2
            )
            ELSE NULL
        END AS official_score
    FROM session_scores
    ORDER BY started_at DESC
    LIMIT 200
";

$sessions = fetch_all_rows($link, $sessionsSql);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="text-primary fw-bold mb-1">
            <i class="fa-solid fa-clock-rotate-left"></i> Historial de sesiones
        </h2>
        <p class="text-secondary small mb-0">Sesiones realizadas, resultados y acceso al detalle.</p>
    </div>

    <div class="d-flex gap-2">
        <a href="progreso_cuestionarios.php" class="btn btn-outline-secondary">
            <i class="fa-solid fa-clipboard-list"></i> Progreso
        </a>
        <a href="estadisticas.php" class="btn btn-outline-primary">
            <i class="fa-solid fa-chart-line"></i> Estadísticas
        </a>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-filter text-primary"></i> Filtros
        </h5>
    </div>

    <div class="card-body">
        <form method="get" action="historial_sesiones.php" class="row g-3 align-items-end">
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

                <a href="historial_sesiones.php" class="btn btn-outline-secondary">
                    <i class="fa-solid fa-xmark"></i>
                </a>
            </div>
        </form>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-list text-primary"></i> Tests realizados
        </h5>
        <span class="badge bg-secondary"><?php echo count($sessions); ?></span>
    </div>

    <div class="card-body">
        <?php if (empty($sessions)): ?>
            <p class="text-secondary mb-0">No hay sesiones registradas con los filtros seleccionados.</p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Categoría</th>
                            <th>Tipo</th>
                            <th class="text-end">Contestadas</th>
                            <th class="text-end">En blanco</th>
                            <th class="text-end">Aciertos</th>
                            <th class="text-end">Fallos</th>
                            <th class="text-end">Resultado</th>
                            <th class="text-end">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($sessions as $row): ?>
                            <?php
                                $isOfficial = is_official_exam_row($row);
                                $hasScoring = has_official_scoring($row);
                                $totalQuestions = (int)$row['total_questions'];
                                $answered = (int)$row['total_answers'];
                                $blank = $isOfficial ? max(0, $totalQuestions - $answered) : null;
                                $detailUrl = 'detalle_sesion.php?session_id=' . urlencode($row['test_session_id']);
                                $repeatUrl = 'test.php?categoria=' . urlencode($row['categoria']);
                            ?>
                            <tr>
                                <td><?php echo safe_text($row['started_at']); ?></td>
                                <td>
                                    <div class="fw-semibold"><?php echo safe_text($row['categoria'] ?: 'Sin categoría'); ?></div>
                                    <?php if (!empty($row['organismo']) || !empty($row['proceso_selectivo']) || !empty($row['convocatoria_year'])): ?>
                                        <div class="text-secondary small">
                                            <?php echo safe_text(trim(($row['organismo'] ?? '') . ' · ' . ($row['proceso_selectivo'] ?? '') . ' · ' . ($row['convocatoria_year'] ?? ''), ' ·')); ?>
                                        </div>
                                    <?php endif; ?>

                                    <?php if ($hasScoring): ?>
                                        <div class="text-secondary small">
                                            Regla: <?php echo safe_text($row['scoring_rule_code']); ?>
                                        </div>
                                    <?php endif; ?>
                                </td>
                                <td><?php echo safe_text($row['tipo'] ?: '-'); ?></td>
                                <td class="text-end"><?php echo $answered; ?></td>
                                <td class="text-end"><?php echo $isOfficial ? (int)$blank : '-'; ?></td>
                                <td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td>
                                <td class="text-end text-danger"><?php echo (int)$row['wrong_answers']; ?></td>
                                <td class="text-end fw-bold">
                                    <?php if ($hasScoring): ?>
                                        <?php echo format_decimal($row['official_score']); ?> / <?php echo format_score_scale($row['score_scale']); ?>
                                    <?php else: ?>
                                        <?php echo format_percentage($row['accuracy_percentage']); ?>
                                    <?php endif; ?>
                                </td>
                                <td class="text-end">
                                    <div class="d-flex gap-2 justify-content-end">
                                        <a href="<?php echo safe_text($detailUrl); ?>" class="btn btn-outline-primary btn-sm">
                                            <i class="fa-solid fa-eye"></i> Detalle
                                        </a>
                                        <a href="<?php echo safe_text($repeatUrl); ?>" class="btn btn-outline-secondary btn-sm">
                                            <i class="fa-solid fa-rotate-right"></i> Repetir
                                        </a>
                                    </div>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <p class="text-secondary small mb-0">
                Se muestran como máximo las 200 sesiones más recientes.
            </p>
        <?php endif; ?>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
