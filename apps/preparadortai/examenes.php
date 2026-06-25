<?php include 'includes/header.php'; ?>

<?php
function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
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

function infer_year_from_category($category) {
    $category = (string)$category;

    if (preg_match('/(20[0-9]{2}|19[0-9]{2})/', $category, $matches)) {
        return $matches[0];
    }

    if (preg_match('/\b([0-9]{2})\b/', $category, $matches)) {
        return '20' . $matches[1];
    }

    return 'Otros';
}

function infer_exam_part($category, $description = '') {
    $text = strtoupper((string)$category . ' ' . (string)$description);

    if (strpos($text, 'PRACT') !== false) {
        return 'Práctico';
    }

    if (strpos($text, 'TEOR') !== false) {
        return 'Teoría';
    }

    return 'General';
}

function normalize_turno($turno) {
    $turno = trim((string)$turno);

    if ($turno === '') {
        return '';
    }

    $upper = strtoupper($turno);

    if ($upper === 'LIBRE') {
        return 'Libre';
    }

    if (strpos($upper, 'PROMOC') !== false || $upper === 'PI') {
        return 'Promoción interna';
    }

    return $turno;
}

function build_exam_title($row) {
    $part = infer_exam_part($row['categoria'], $row['descripcion'] ?? '');
    $turno = normalize_turno($row['turno'] ?? '');

    if ($turno !== '') {
        return $part . ' · ' . $turno;
    }

    return $part;
}

function build_group_label($organismo, $proceso) {
    $organismo = trim((string)$organismo);
    $proceso = trim((string)$proceso);

    if ($organismo !== '' && $proceso !== '') {
        return $organismo . ' · ' . $proceso;
    }

    if ($organismo !== '') {
        return $organismo;
    }

    if ($proceso !== '') {
        return $proceso;
    }

    return 'Otros exámenes';
}

$filterOrganismo = isset($_GET['organismo']) ? trim($_GET['organismo']) : '';
$filterProceso = isset($_GET['proceso_selectivo']) ? trim($_GET['proceso_selectivo']) : '';
$filterYear = isset($_GET['year']) ? trim($_GET['year']) : '';
$filterTurno = isset($_GET['turno']) ? trim($_GET['turno']) : '';

$whereClauses = [
    "(COALESCE(qs.tipo, '') = 'Examen oficial' OR p.categoria LIKE '%CUESTIONARIO%')"
];

if ($filterOrganismo !== '') {
    $whereClauses[] = "COALESCE(qs.organismo, '') = '" . mysqli_real_escape_string($link, $filterOrganismo) . "'";
}

if ($filterProceso !== '') {
    $whereClauses[] = "COALESCE(qs.proceso_selectivo, '') = '" . mysqli_real_escape_string($link, $filterProceso) . "'";
}

if ($filterYear !== '') {
    $whereClauses[] = "COALESCE(qs.convocatoria_year, 0) = " . (int)$filterYear;
}

if ($filterTurno !== '') {
    $whereClauses[] = "COALESCE(qs.turno, '') = '" . mysqli_real_escape_string($link, $filterTurno) . "'";
}

$whereSql = 'WHERE ' . implode(' AND ', $whereClauses);

$organismos = fetch_all_rows($link, "
    SELECT DISTINCT organismo
    FROM question_sets
    WHERE tipo = 'Examen oficial'
      AND organismo IS NOT NULL
      AND organismo <> ''
    ORDER BY organismo
");

$procesos = fetch_all_rows($link, "
    SELECT DISTINCT proceso_selectivo
    FROM question_sets
    WHERE tipo = 'Examen oficial'
      AND proceso_selectivo IS NOT NULL
      AND proceso_selectivo <> ''
    ORDER BY proceso_selectivo
");

$years = fetch_all_rows($link, "
    SELECT DISTINCT convocatoria_year
    FROM question_sets
    WHERE tipo = 'Examen oficial'
      AND convocatoria_year IS NOT NULL
    ORDER BY convocatoria_year DESC
");

$turnos = fetch_all_rows($link, "
    SELECT DISTINCT turno
    FROM question_sets
    WHERE tipo = 'Examen oficial'
      AND turno IS NOT NULL
      AND turno <> ''
    ORDER BY turno
");

$sql = "
    SELECT
        p.categoria,
        COUNT(*) AS total_questions,
        qs.id AS question_set_id,
        qs.organismo,
        qs.proceso_selectivo,
        qs.convocatoria_year,
        qs.turno,
        qs.tipo,
        qs.descripcion
    FROM ptype p
    LEFT JOIN question_sets qs
        ON qs.categoria = p.categoria
    $whereSql
    GROUP BY
        p.categoria,
        qs.id,
        qs.organismo,
        qs.proceso_selectivo,
        qs.convocatoria_year,
        qs.turno,
        qs.tipo,
        qs.descripcion
    ORDER BY
        COALESCE(qs.organismo, 'ZZZ') ASC,
        COALESCE(qs.proceso_selectivo, 'ZZZ') ASC,
        COALESCE(qs.convocatoria_year, 0) DESC,
        p.categoria ASC
";

$result = mysqli_query($link, $sql);
$groups = [];

if ($result && mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        $group = build_group_label($row['organismo'], $row['proceso_selectivo']);
        $year = !empty($row['convocatoria_year'])
            ? (string)$row['convocatoria_year']
            : infer_year_from_category($row['categoria']);

        $groups[$group][$year][] = [
            'title' => build_exam_title($row),
            'category' => $row['categoria'],
            'description' => $row['descripcion'] ?? '',
            'questions' => (int)$row['total_questions'],
            'question_set_id' => (int)($row['question_set_id'] ?? 0),
        ];
    }

    foreach ($groups as &$yearsGroup) {
        krsort($yearsGroup);
    }
    unset($yearsGroup);
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1">Exámenes Oficiales</h2>
        <p class="text-secondary small mb-0">Exámenes agrupados por organismo, proceso y convocatoria.</p>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-filter text-primary"></i> Filtros
        </h5>
    </div>

    <div class="card-body">
        <form method="get" action="examenes.php" class="row g-3 align-items-end">
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
                <label for="turno" class="form-label">Turno</label>
                <select id="turno" name="turno" class="form-select">
                    <option value="">Todos</option>
                    <?php foreach ($turnos as $row): ?>
                        <option value="<?php echo safe_text($row['turno']); ?>" <?php echo $filterTurno === $row['turno'] ? 'selected' : ''; ?>>
                            <?php echo safe_text(normalize_turno($row['turno'])); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="col-md-2 d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    <i class="fa-solid fa-filter"></i> Filtrar
                </button>

                <a href="examenes.php" class="btn btn-outline-secondary">
                    Limpiar
                </a>
            </div>
        </form>
    </div>
</div>

<?php if (empty($groups)): ?>
    <div class="alert alert-warning">No hay exámenes cargados con los filtros seleccionados.</div>
<?php else: ?>
    <?php foreach ($groups as $groupLabel => $yearsGroup): ?>
        <div class="mb-5">
            <h4 class="fw-bold text-dark mb-3">
                <i class="fa-solid fa-building-columns text-primary"></i>
                <?php echo safe_text($groupLabel); ?>
            </h4>

            <div class="row g-4">
                <?php foreach ($yearsGroup as $year => $exams): ?>
                    <div class="col-md-6 col-xl-4">
                        <div class="card h-100 shadow-sm border-0 year-card">
                            <div class="card-header border-0 bg-transparent pt-4 px-4 d-flex align-items-center">
                                <div class="rounded-3 bg-danger bg-opacity-10 text-danger p-2 me-3 text-center" style="min-width: 50px;">
                                    <i class="fa-solid fa-calendar-days fs-4"></i>
                                </div>
                                <div>
                                    <h4 class="fw-bold text-dark mb-0"><?php echo safe_text($year); ?></h4>
                                    <span class="text-muted small"><?php echo count($exams); ?> exámenes</span>
                                </div>
                            </div>

                            <div class="card-body px-4 pb-4">
                                <hr class="text-muted opacity-25 mt-0 mb-3">

                                <div class="d-flex flex-column gap-2">
                                    <?php foreach ($exams as $exam): ?>
                                        <div class="d-flex gap-2 align-items-stretch">
                                            <a href="test.php?categoria=<?php echo urlencode($exam['category']); ?>"
                                               class="btn btn-outline-secondary btn-sm rounded-pill px-3 py-2 flex-grow-1 text-start btn-opcion"
                                               title="<?php echo safe_text($exam['category']); ?>">
                                                <span class="fw-semibold"><?php echo safe_text($exam['title']); ?></span>
                                                <span class="badge bg-light text-secondary border ms-1"><?php echo (int)$exam['questions']; ?></span>
                                            </a>
                                        </div>
                                    <?php endforeach; ?>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    <?php endforeach; ?>
<?php endif; ?>

<style>
.year-card {
    transition: transform 0.2s, box-shadow 0.2s;
    background: #fff;
}
.year-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
}
.btn-opcion {
    border-color: #e2e8f0;
    color: #64748b;
    font-weight: 500;
    font-size: 0.85rem;
    transition: all 0.2s;
    background-color: #f8fafc;
}
.btn-opcion:hover {
    background-color: #fee2e2;
    border-color: #ef4444;
    color: #b91c1c;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.1);
}
</style>

<?php include 'includes/footer.php'; ?>
