<?php include 'includes/header.php'; ?>

<?php
function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function truncate_text($value, $length = 80) {
    $value = (string)($value ?? '');

    if (function_exists('mb_strlen') && function_exists('mb_substr')) {
        return mb_strlen($value) > $length ? mb_substr($value, 0, $length) . '...' : $value;
    }

    return strlen($value) > $length ? substr($value, 0, $length) . '...' : $value;
}

function has_category_info($row) {
    return !empty($row['organismo'])
        || !empty($row['proceso_selectivo'])
        || !empty($row['convocatoria_year'])
        || !empty($row['turno'])
        || !empty($row['tipo'])
        || !empty($row['descripcion']);
}

function bind_dynamic_params($stmt, $types, $params) {
    if ($types === '' || empty($params)) {
        return;
    }

    $refs = [];
    $refs[] = $types;

    foreach ($params as $key => $value) {
        $refs[] = &$params[$key];
    }

    call_user_func_array([$stmt, 'bind_param'], $refs);
}

function fetch_all_rows($link, $sql, $types = '', $params = []) {
    $stmt = mysqli_prepare($link, $sql);

    if (!$stmt) {
        return [];
    }

    bind_dynamic_params($stmt, $types, $params);

    mysqli_stmt_execute($stmt);
    $res = mysqli_stmt_get_result($stmt);
    $rows = [];

    while ($row = mysqli_fetch_assoc($res)) {
        $rows[] = $row;
    }

    mysqli_stmt_close($stmt);

    return $rows;
}

$filtroCategoria = trim((string)($_GET['categoria'] ?? ''));
$filtroBloque = trim((string)($_GET['bloque'] ?? ''));
$filtroTema = trim((string)($_GET['tema'] ?? ''));
$filtroTexto = trim((string)($_GET['texto'] ?? ''));

$hayFiltros = $filtroCategoria !== ''
    || $filtroBloque !== ''
    || $filtroTema !== ''
    || $filtroTexto !== '';

$categories = [];
$sqlCategories = "
    SELECT categoria
    FROM question_sets
    WHERE categoria IS NOT NULL AND categoria <> ''

    UNION

    SELECT DISTINCT categoria
    FROM ptype
    WHERE categoria IS NOT NULL AND categoria <> ''

    UNION

    SELECT DISTINCT categoria
    FROM rtype
    WHERE categoria IS NOT NULL AND categoria <> ''

    ORDER BY categoria
";
$resCategories = mysqli_query($link, $sqlCategories);

while ($row = mysqli_fetch_assoc($resCategories)) {
    $categories[] = $row['categoria'];
}

$ptypeWhere = [];
$ptypeTypes = '';
$ptypeParams = [];

if ($filtroCategoria !== '') {
    $ptypeWhere[] = 'p.categoria = ?';
    $ptypeTypes .= 's';
    $ptypeParams[] = $filtroCategoria;
}

if ($filtroBloque !== '') {
    $ptypeWhere[] = 'p.bloque = ?';
    $ptypeTypes .= 's';
    $ptypeParams[] = $filtroBloque;
}

if ($filtroTema !== '') {
    $ptypeWhere[] = 'p.tema = ?';
    $ptypeTypes .= 's';
    $ptypeParams[] = $filtroTema;
}

if ($filtroTexto !== '') {
    $ptypeWhere[] = '(p.pregunta LIKE ? OR p.respuesta LIKE ? OR p.categoria LIKE ?)';
    $ptypeTypes .= 'sss';
    $search = '%' . $filtroTexto . '%';
    $ptypeParams[] = $search;
    $ptypeParams[] = $search;
    $ptypeParams[] = $search;
}

$ptypeWhereSql = empty($ptypeWhere) ? '' : 'WHERE ' . implode(' AND ', $ptypeWhere);

$sqlPtype = "
    SELECT
        p.*,
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
    $ptypeWhereSql
    ORDER BY p.id DESC
";

$ptypeRows = fetch_all_rows($link, $sqlPtype, $ptypeTypes, $ptypeParams);

$rtypeWhere = [];
$rtypeTypes = '';
$rtypeParams = [];

if ($filtroBloque !== '' || $filtroTema !== '') {
    $rtypeWhere[] = '1 = 0';
}

if ($filtroCategoria !== '') {
    $rtypeWhere[] = 'r.categoria = ?';
    $rtypeTypes .= 's';
    $rtypeParams[] = $filtroCategoria;
}

if ($filtroTexto !== '') {
    $rtypeWhere[] = '(r.pregunta LIKE ? OR r.respuesta LIKE ? OR r.categoria LIKE ?)';
    $rtypeTypes .= 'sss';
    $search = '%' . $filtroTexto . '%';
    $rtypeParams[] = $search;
    $rtypeParams[] = $search;
    $rtypeParams[] = $search;
}

$rtypeWhereSql = empty($rtypeWhere) ? '' : 'WHERE ' . implode(' AND ', $rtypeWhere);

$sqlRtype = "
    SELECT
        r.*,
        qs.id AS question_set_id,
        qs.organismo,
        qs.proceso_selectivo,
        qs.convocatoria_year,
        qs.turno,
        qs.tipo,
        qs.descripcion
    FROM rtype r
    LEFT JOIN question_sets qs
        ON qs.categoria = r.categoria
    $rtypeWhereSql
    ORDER BY r.id DESC
";

$rtypeRows = fetch_all_rows($link, $sqlRtype, $rtypeTypes, $rtypeParams);
?>

<link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css">

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1"><i class="fa-solid fa-database"></i> Banco de Preguntas</h2>
        <p class="text-secondary small mb-0">Gestiona, edita o elimina preguntas de tu base de datos.</p>
    </div>

    <div class="d-flex gap-2">
        <a href="progreso_cuestionarios.php" class="btn btn-outline-primary rounded-pill shadow-sm">
            <i class="fa-solid fa-clipboard-list"></i> Progreso
        </a>

        <a href="nueva_categoria.php" class="btn btn-outline-success rounded-pill shadow-sm">
            <i class="fa-solid fa-folder-plus"></i> Nueva Categoría
        </a>

        <a href="agregar.php" class="btn btn-success rounded-pill shadow-sm">
            <i class="fa-solid fa-plus"></i> Nueva Pregunta
        </a>
    </div>
</div>

<div class="card border-0 shadow-sm mb-3">
    <div class="card-body">
        <form method="get" action="gestionar.php">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-bold mb-0"><i class="fa-solid fa-filter"></i> Filtros</h5>

                <div class="d-flex gap-2">
                    <a href="gestionar.php" class="btn btn-sm btn-outline-secondary">
                        <i class="fa-solid fa-eraser"></i> Limpiar
                    </a>

                    <button type="submit" class="btn btn-sm btn-primary">
                        <i class="fa-solid fa-magnifying-glass"></i> Aplicar filtros
                    </button>
                </div>
            </div>

            <div class="row g-3">
                <div class="col-lg-4">
                    <label for="categoria" class="form-label small fw-bold">Categoría</label>
                    <select id="categoria" name="categoria" class="form-select form-select-sm">
                        <option value="">Todas</option>
                        <?php foreach ($categories as $category): ?>
                            <option value="<?php echo safe_text($category); ?>" <?php echo $filtroCategoria === $category ? 'selected' : ''; ?>>
                                <?php echo safe_text($category); ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div class="col-lg-2 col-md-3">
                    <label for="bloque" class="form-label small fw-bold">Bloque</label>
                    <input type="number" id="bloque" name="bloque" class="form-control form-control-sm" value="<?php echo safe_text($filtroBloque); ?>" placeholder="Ej. 2">
                </div>

                <div class="col-lg-2 col-md-3">
                    <label for="tema" class="form-label small fw-bold">Tema</label>
                    <input type="number" id="tema" name="tema" class="form-control form-control-sm" value="<?php echo safe_text($filtroTema); ?>" placeholder="Ej. 5">
                </div>

                <div class="col-lg-4 col-md-6">
                    <label for="texto" class="form-label small fw-bold">Texto en pregunta/respuesta</label>
                    <input type="text" id="texto" name="texto" class="form-control form-control-sm" value="<?php echo safe_text($filtroTexto); ?>" placeholder="Buscar texto...">
                </div>
            </div>
        </form>

        <?php if ($hayFiltros): ?>
            <div class="alert alert-light border mt-3 mb-0 small">
                Resultados filtrados:
                <strong><?php echo count($ptypeRows); ?></strong> preguntas tipo test
                y <strong><?php echo count($rtypeRows); ?></strong> preguntas de relacionar.
            </div>
        <?php endif; ?>
    </div>
</div>

<ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
    <li class="nav-item" role="presentation">
        <button class="nav-link active fw-bold" id="test-tab" data-bs-toggle="tab" data-bs-target="#test-pane" type="button" role="tab"><i class="fa-solid fa-list-ul"></i> Tipo Test (Ptype)</button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link fw-bold" id="rel-tab" data-bs-toggle="tab" data-bs-target="#rel-pane" type="button" role="tab"><i class="fa-solid fa-arrows-left-right"></i> Relacionar (Rtype)</button>
    </li>
</ul>

<div class="tab-content" id="myTabContent">

    <div class="tab-pane fade show active bg-white p-4 border border-top-0 rounded-bottom shadow-sm" id="test-pane" role="tabpanel">
        <table id="tablaTest" class="table table-hover align-middle w-100">
            <thead class="table-light">
                <tr>
                    <th style="width: 5%">ID</th>
                    <th style="width: 18%">Categoría</th>
                    <th style="width: 47%">Pregunta</th>
                    <th style="width: 15%">Tema/Bloque</th>
                    <th style="width: 15%">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach($ptypeRows as $row){ ?>
                <tr>
                    <td><span class="badge bg-secondary"><?php echo (int)$row['id']; ?></span></td>

                    <td>
                        <small class="fw-bold text-primary"><?php echo safe_text($row['categoria']); ?></small>

                        <div class="mt-1 d-flex gap-1 flex-wrap">
                            <?php if (has_category_info($row)): ?>
                                <button type="button"
                                        class="btn btn-sm btn-outline-secondary py-0 px-2"
                                        onclick="mostrarInfoCategoria(this)"
                                        data-categoria="<?php echo safe_text($row['categoria']); ?>"
                                        data-organismo="<?php echo safe_text($row['organismo']); ?>"
                                        data-proceso="<?php echo safe_text($row['proceso_selectivo']); ?>"
                                        data-year="<?php echo safe_text($row['convocatoria_year']); ?>"
                                        data-turno="<?php echo safe_text($row['turno']); ?>"
                                        data-tipo="<?php echo safe_text($row['tipo']); ?>"
                                        data-descripcion="<?php echo safe_text($row['descripcion']); ?>">
                                    <i class="fa-solid fa-circle-info"></i> Info
                                </button>
                            <?php else: ?>
                                <span class="badge bg-warning text-dark">Sin info</span>
                            <?php endif; ?>

                            <?php if (!empty($row['question_set_id'])): ?>
                                <a href="editar_cuestionario.php?id=<?php echo (int)$row['question_set_id']; ?>" class="btn btn-sm btn-outline-dark py-0 px-2" title="Editar información de categoría">
                                    <i class="fa-solid fa-pen"></i>
                                </a>
                            <?php endif; ?>
                        </div>
                    </td>

                    <td>
                        <?php echo safe_text(truncate_text($row['pregunta'], 90)); ?>
                        <br><small class="text-muted"><i class="fa-solid fa-check text-success"></i> <?php echo safe_text($row['respuesta']); ?></small>
                    </td>

                    <td><small class="badge bg-light text-dark border">B:<?php echo safe_text($row['bloque']); ?> / T:<?php echo safe_text($row['tema']); ?></small></td>

                    <td>
                        <a href="editar.php?id=<?php echo (int)$row['id']; ?>&type=ptype" class="btn btn-sm btn-outline-primary" title="Editar"><i class="fa-solid fa-pen"></i></a>
                        <button onclick="confirmarBorrado(<?php echo (int)$row['id']; ?>, 'ptype')" class="btn btn-sm btn-outline-danger" title="Eliminar"><i class="fa-solid fa-trash"></i></button>
                    </td>
                </tr>
                <?php } ?>
            </tbody>
        </table>
    </div>

    <div class="tab-pane fade bg-white p-4 border border-top-0 rounded-bottom shadow-sm" id="rel-pane" role="tabpanel">
        <table id="tablaRel" class="table table-hover align-middle w-100">
            <thead class="table-light">
                <tr>
                    <th style="width: 5%">ID</th>
                    <th style="width: 18%">Categoría</th>
                    <th style="width: 32%">Pregunta (Concepto)</th>
                    <th style="width: 30%">Respuesta (Definición)</th>
                    <th style="width: 15%">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach($rtypeRows as $row){ ?>
                <tr>
                    <td><span class="badge bg-secondary"><?php echo (int)$row['id']; ?></span></td>

                    <td>
                        <small class="fw-bold text-success"><?php echo safe_text($row['categoria']); ?></small>

                        <div class="mt-1 d-flex gap-1 flex-wrap">
                            <?php if (has_category_info($row)): ?>
                                <button type="button"
                                        class="btn btn-sm btn-outline-secondary py-0 px-2"
                                        onclick="mostrarInfoCategoria(this)"
                                        data-categoria="<?php echo safe_text($row['categoria']); ?>"
                                        data-organismo="<?php echo safe_text($row['organismo']); ?>"
                                        data-proceso="<?php echo safe_text($row['proceso_selectivo']); ?>"
                                        data-year="<?php echo safe_text($row['convocatoria_year']); ?>"
                                        data-turno="<?php echo safe_text($row['turno']); ?>"
                                        data-tipo="<?php echo safe_text($row['tipo']); ?>"
                                        data-descripcion="<?php echo safe_text($row['descripcion']); ?>">
                                    <i class="fa-solid fa-circle-info"></i> Info
                                </button>
                            <?php else: ?>
                                <span class="badge bg-warning text-dark">Sin info</span>
                            <?php endif; ?>

                            <?php if (!empty($row['question_set_id'])): ?>
                                <a href="editar_cuestionario.php?id=<?php echo (int)$row['question_set_id']; ?>" class="btn btn-sm btn-outline-dark py-0 px-2" title="Editar información de categoría">
                                    <i class="fa-solid fa-pen"></i>
                                </a>
                            <?php endif; ?>
                        </div>
                    </td>

                    <td><?php echo safe_text($row['pregunta']); ?></td>
                    <td><small class="text-muted"><?php echo safe_text(truncate_text($row['respuesta'], 60)); ?></small></td>

                    <td>
                        <a href="editar.php?id=<?php echo (int)$row['id']; ?>&type=rtype" class="btn btn-sm btn-outline-primary"><i class="fa-solid fa-pen"></i></a>
                        <button onclick="confirmarBorrado(<?php echo (int)$row['id']; ?>, 'rtype')" class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-trash"></i></button>
                    </td>
                </tr>
                <?php } ?>
            </tbody>
        </table>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.5.1.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

<script>
    $(document).ready(function () {
        var opciones = {
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json"
            },
            "pageLength": 10,
            "order": [[ 0, "desc" ]]
        };

        $('#tablaTest').DataTable(opciones);
        $('#tablaRel').DataTable(opciones);
    });

    function mostrarInfoCategoria(button) {
        const info = button.dataset;

        const html = `
            <div class="text-start">
                <p class="mb-1"><strong>Organismo:</strong> ${info.organismo || '-'}</p>
                <p class="mb-1"><strong>Proceso selectivo:</strong> ${info.proceso || '-'}</p>
                <p class="mb-1"><strong>Año:</strong> ${info.year || '-'}</p>
                <p class="mb-1"><strong>Turno:</strong> ${info.turno || '-'}</p>
                <p class="mb-1"><strong>Tipo:</strong> ${info.tipo || '-'}</p>
                ${info.descripcion ? `<p class="mb-0"><strong>Notas:</strong> ${info.descripcion}</p>` : ''}
            </div>
        `;

        Swal.fire({
            title: info.categoria || 'Información de categoría',
            html: html,
            icon: 'info',
            confirmButtonText: 'Cerrar'
        });
    }

    function confirmarBorrado(id, type) {
        Swal.fire({
            title: '¿Estás seguro?',
            text: "No podrás revertir esto. Se borrará la pregunta y sus respuestas.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, borrar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.post('logic/delete.php', {id: id, type: type}, function(response) {
                    if(response.trim() == 'success') {
                        Swal.fire('¡Borrado!', 'La pregunta ha sido eliminada.', 'success')
                        .then(() => location.reload());
                    } else {
                        Swal.fire('Error', 'Hubo un problema al borrar: ' + response, 'error');
                    }
                });
            }
        })
    }
</script>

<?php include 'includes/footer.php'; ?>
