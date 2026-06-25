<?php include 'includes/header.php'; ?>

<?php
function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
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

function clean_exam_title($row) {
    $categoria = (string)$row['categoria'];

    if (!empty($row['descripcion'])) {
        $title = $row['descripcion'];
    } else {
        $title = $categoria;
        $title = str_ireplace('CUESTIONARIO', '', $title);
        $title = str_replace((string)$row['convocatoria_year'], '', $title);

        if (!empty($row['convocatoria_year'])) {
            $title = str_replace(substr((string)$row['convocatoria_year'], 2), '', $title);
        }

        $title = trim($title, " -_");
    }

    if (!empty($row['turno'])) {
        $title .= ' · ' . $row['turno'];
    }

    if (trim($title) === '' || strlen(trim($title)) < 2) {
        $title = 'General';
    }

    return strtoupper($title);
}

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
    WHERE
        COALESCE(qs.tipo, '') = 'Examen oficial'
        OR p.categoria LIKE '%CUESTIONARIO%'
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
        COALESCE(qs.convocatoria_year, 0) DESC,
        p.categoria ASC
";

$result = mysqli_query($link, $sql);
$examenesPorAnio = [];

if ($result && mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        $anio = !empty($row['convocatoria_year'])
            ? (string)$row['convocatoria_year']
            : infer_year_from_category($row['categoria']);

        $examenesPorAnio[$anio][] = [
            'titulo' => clean_exam_title($row),
            'full_cat' => $row['categoria'],
            'organismo' => $row['organismo'] ?: '',
            'proceso' => $row['proceso_selectivo'] ?: '',
            'questions' => (int)$row['total_questions'],
        ];
    }

    krsort($examenesPorAnio);
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1">Exámenes Oficiales</h2>
        <p class="text-secondary small mb-0">Histórico de convocatorias agrupadas por año.</p>
    </div>
</div>

<?php if (empty($examenesPorAnio)): ?>
    <div class="alert alert-warning">No hay exámenes cargados.</div>
<?php else: ?>
    <div class="row g-4">
        <?php foreach ($examenesPorAnio as $anio => $listaExamenes): ?>
            <div class="col-md-6 col-xl-4">
                <div class="card h-100 shadow-sm border-0 year-card">

                    <div class="card-header border-0 bg-transparent pt-4 px-4 d-flex align-items-center">
                        <div class="rounded-3 bg-danger bg-opacity-10 text-danger p-2 me-3 text-center" style="min-width: 50px;">
                            <i class="fa-solid fa-calendar-days fs-4"></i>
                        </div>
                        <div>
                            <h4 class="fw-bold text-dark mb-0"><?php echo safe_text($anio); ?></h4>
                            <span class="text-muted small"><?php echo count($listaExamenes); ?> exámenes</span>
                        </div>
                    </div>

                    <div class="card-body px-4 pb-4">
                        <hr class="text-muted opacity-25 mt-0 mb-3">

                        <div class="d-flex flex-wrap gap-2">
                            <?php foreach ($listaExamenes as $ex): ?>
                                <a href="test.php?categoria=<?php echo urlencode($ex['full_cat']); ?>"
                                   class="btn btn-outline-secondary btn-sm rounded-pill px-3 py-2 flex-grow-1 text-truncate btn-opcion"
                                   title="<?php echo safe_text($ex['full_cat']); ?>">
                                    <?php echo safe_text($ex['titulo']); ?>
                                    <span class="badge bg-light text-secondary border ms-1"><?php echo (int)$ex['questions']; ?></span>
                                </a>
                            <?php endforeach; ?>
                        </div>
                    </div>

                </div>
            </div>
        <?php endforeach; ?>
    </div>
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
