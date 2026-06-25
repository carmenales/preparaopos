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

$filterOrganismo = isset($_GET['organismo']) ? trim($_GET['organismo']) : '';
$filterProceso = isset($_GET['proceso_selectivo']) ? trim($_GET['proceso_selectivo']) : '';
$filterYear = isset($_GET['year']) ? trim($_GET['year']) : '';
$filterTipo = isset($_GET['tipo']) ? trim($_GET['tipo']) : '';
$filterText = isset($_GET['q']) ? trim($_GET['q']) : '';

$whereClauses = [];

if ($filterOrganismo !== '') {
    $whereClauses[] = "COALESCE(qs.organismo, '') = '" . mysqli_real_escape_string($link, $filterOrganismo) . "'";
}

if ($filterProceso !== '') {
    $whereClauses[] = "COALESCE(qs.proceso_selectivo, '') = '" . mysqli_real_escape_string($link, $filterProceso) . "'";
}

if ($filterYear !== '') {
    $whereClauses[] = "qs.convocatoria_year = " . (int)$filterYear;
}

if ($filterTipo !== '') {
    $whereClauses[] = "COALESCE(qs.tipo, '') = '" . mysqli_real_escape_string($link, $filterTipo) . "'";
}

if ($filterText !== '') {
    $escapedText = mysqli_real_escape_string($link, $filterText);
    $whereClauses[] = "(
        qc.categoria LIKE '%$escapedText%'
        OR COALESCE(qs.descripcion, '') LIKE '%$escapedText%'
        OR COALESCE(qs.organismo, '') LIKE '%$escapedText%'
        OR COALESCE(qs.proceso_selectivo, '') LIKE '%$escapedText%'
    )";
}

$filterSql = empty($whereClauses) ? '' : 'WHERE ' . implode(' AND ', $whereClauses);

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

$missingMetadataRows = fetch_all_rows($link, "
    SELECT COUNT(DISTINCT p.categoria) AS total
    FROM ptype p
    LEFT JOIN question_sets qs
        ON qs.categoria = p.categoria
    WHERE
        p.categoria IS NOT NULL
        AND p.categoria <> ''
        AND qs.id IS NULL
");

$missingMetadataCount = (int)($missingMetadataRows[0]['total'] ?? 0);
$syncedQuestionSets = isset($_GET['synced_question_sets']) ? (int)$_GET['synced_question_sets'] : null;
$updatedQuestionSet = isset($_GET['updated_question_set']) ? (int)$_GET['updated_question_set'] : 0;

$categoriesSql = "
    WITH question_counts AS (
        SELECT
            categoria,
            COUNT(*) AS total_questions
        FROM ptype
        WHERE categoria IS NOT NULL AND categoria <> ''
        GROUP BY categoria
    )
    SELECT
        qc.categoria,
        qc.total_questions,
        qs.id AS question_set_id,
        qs.organismo,
        qs.proceso_selectivo,
        qs.convocatoria_year,
        qs.turno,
        qs.tipo,
        qs.descripcion
    FROM question_counts qc
    LEFT JOIN question_sets qs
        ON qs.categoria = qc.categoria
    $filterSql
    ORDER BY
        CASE WHEN qs.id IS NULL THEN 0 ELSE 1 END ASC,
        COALESCE(qs.organismo, 'ZZZ') ASC,
        COALESCE(qs.proceso_selectivo, 'ZZZ') ASC,
        COALESCE(qs.convocatoria_year, 0) DESC,
        qc.categoria ASC
";

$categories = fetch_all_rows($link, $categoriesSql);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="text-primary fw-bold mb-1">
            <i class="fa-solid fa-tags"></i> Categorías
        </h2>
        <p class="text-secondary small mb-0">Administración de categorías, cuestionarios y metadatos.</p>
    </div>

    <div class="d-flex gap-2">
        <form method="post" action="logic/sync_question_sets.php">
            <button type="submit" class="btn btn-outline-secondary" <?php echo $missingMetadataCount === 0 ? 'disabled' : ''; ?>>
                <i class="fa-solid fa-rotate"></i> Sincronizar
                <?php if ($missingMetadataCount > 0): ?>
                    <span class="badge bg-danger ms-1"><?php echo $missingMetadataCount; ?></span>
                <?php endif; ?>
            </button>
        </form>

        <a href="nueva_categoria.php" class="btn btn-primary">
            <i class="fa-solid fa-plus"></i> Nueva categoría
        </a>
    </div>
</div>

<?php if ($updatedQuestionSet === 1): ?>
    <div class="alert alert-success shadow-sm border-0">
        Metadatos actualizados correctamente.
    </div>
<?php endif; ?>

<?php if ($syncedQuestionSets !== null): ?>
    <div class="alert alert-success shadow-sm border-0">
        Se han creado <?php echo $syncedQuestionSets; ?> registros de metadatos.
    </div>
<?php endif; ?>

<?php if ($missingMetadataCount > 0): ?>
    <div class="alert alert-warning shadow-sm border-0">
        Hay <?php echo $missingMetadataCount; ?> categorías con preguntas pero sin metadatos.
    </div>
<?php endif; ?>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-filter text-primary"></i> Filtros
        </h5>
    </div>

    <div class="card-body">
        <form method="get" action="categorias.php" class="row g-3 align-items-end">
            <div class="col-md-3">
                <label for="q" class="form-label">Buscar</label>
                <input type="text" id="q" name="q" class="form-control" value="<?php echo safe_text($filterText); ?>" placeholder="Categoría, descripción...">
            </div>

            <div class="col-md-2">
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

            <div class="col-md-2">
                <label for="proceso_selectivo" class="form-label">Proceso</label>
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

            <div class="col-md-1 d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    <i class="fa-solid fa-filter"></i>
                </button>

                <a href="categorias.php" class="btn btn-outline-secondary">
                    <i class="fa-solid fa-xmark"></i>
                </a>
            </div>
        </form>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-list text-primary"></i> Categorías disponibles
        </h5>
        <span class="badge bg-secondary"><?php echo count($categories); ?></span>
    </div>

    <div class="card-body">
        <?php if (empty($categories)): ?>
            <p class="text-secondary mb-0">No hay categorías con los filtros seleccionados.</p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Categoría</th>
                            <th>Organismo</th>
                            <th>Proceso</th>
                            <th class="text-end">Año</th>
                            <th>Turno</th>
                            <th>Tipo</th>
                            <th class="text-end">Preguntas</th>
                            <th class="text-end">Acciones</th>
                        </tr>
                    </thead>

                    <tbody>
                        <?php foreach ($categories as $row): ?>
                            <?php
                                $questionSetId = (int)($row['question_set_id'] ?? 0);
                                $category = $row['categoria'];
                                $testUrl = 'test.php?categoria=' . urlencode($category);
                                $bankUrl = 'gestionar.php?categoria=' . urlencode($category);
                                $editUrl = $questionSetId > 0 ? 'editar_cuestionario.php?id=' . $questionSetId : null;
                            ?>

                            <tr>
                                <td>
                                    <div class="fw-semibold"><?php echo safe_text($category); ?></div>
                                    <?php if (!empty($row['descripcion'])): ?>
                                        <div class="text-secondary small"><?php echo safe_text($row['descripcion']); ?></div>
                                    <?php elseif ($questionSetId === 0): ?>
                                        <div class="text-warning small">Sin metadatos</div>
                                    <?php endif; ?>
                                </td>
                                <td><?php echo safe_text($row['organismo'] ?: '-'); ?></td>
                                <td><?php echo safe_text($row['proceso_selectivo'] ?: '-'); ?></td>
                                <td class="text-end"><?php echo safe_text($row['convocatoria_year'] ?: '-'); ?></td>
                                <td><?php echo safe_text($row['turno'] ?: '-'); ?></td>
                                <td><?php echo safe_text($row['tipo'] ?: '-'); ?></td>
                                <td class="text-end"><?php echo (int)$row['total_questions']; ?></td>
                                <td class="text-end">
                                    <div class="d-flex gap-2 justify-content-end">
                                        <?php if ($editUrl): ?>
                                            <a href="<?php echo safe_text($editUrl); ?>" class="btn btn-outline-dark btn-sm">
                                                <i class="fa-solid fa-pen"></i> Editar
                                            </a>
                                        <?php endif; ?>

                                        <a href="<?php echo safe_text($bankUrl); ?>" class="btn btn-outline-secondary btn-sm">
                                            <i class="fa-solid fa-database"></i> Preguntas
                                        </a>

                                        <a href="<?php echo safe_text($testUrl); ?>" class="btn btn-outline-primary btn-sm">
                                            <i class="fa-solid fa-play"></i> Test
                                        </a>
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
