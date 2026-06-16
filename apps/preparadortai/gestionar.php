<?php include 'includes/header.php'; ?>

<link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css">

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1"><i class="fa-solid fa-database"></i> Banco de Preguntas</h2>
        <p class="text-secondary small mb-0">Gestiona, edita o elimina preguntas de tu base de datos.</p>
    </div>
    <a href="agregar.php" class="btn btn-success rounded-pill shadow-sm">
        <i class="fa-solid fa-plus"></i> Nueva Pregunta
    </a>
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
                    <th style="width: 15%">Categoría</th>
                    <th style="width: 50%">Pregunta</th>
                    <th style="width: 15%">Tema/Bloque</th>
                    <th style="width: 15%">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $sql = "SELECT * FROM ptype ORDER BY id DESC";
                $res = mysqli_query($link, $sql);
                while($row = mysqli_fetch_assoc($res)){
                ?>
                <tr>
                    <td><span class="badge bg-secondary"><?php echo $row['id']; ?></span></td>
                    <td><small class="fw-bold text-primary"><?php echo $row['categoria']; ?></small></td>
                    <td>
                        <?php echo substr($row['pregunta'], 0, 80) . (strlen($row['pregunta']) > 80 ? '...' : ''); ?>
                        <br><small class="text-muted"><i class="fa-solid fa-check text-success"></i> <?php echo $row['respuesta']; ?></small>
                    </td>
                    <td><small class="badge bg-light text-dark border">B:<?php echo $row['bloque']; ?> / T:<?php echo $row['tema']; ?></small></td>
                    <td>
                        <a href="editar.php?id=<?php echo $row['id']; ?>&type=ptype" class="btn btn-sm btn-outline-primary" title="Editar"><i class="fa-solid fa-pen"></i></a>
                        <button onclick="confirmarBorrado(<?php echo $row['id']; ?>, 'ptype')" class="btn btn-sm btn-outline-danger" title="Eliminar"><i class="fa-solid fa-trash"></i></button>
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
                    <th style="width: 15%">Categoría</th>
                    <th style="width: 35%">Pregunta (Concepto)</th>
                    <th style="width: 30%">Respuesta (Definición)</th>
                    <th style="width: 15%">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $sql = "SELECT * FROM rtype ORDER BY id DESC";
                $res = mysqli_query($link, $sql);
                while($row = mysqli_fetch_assoc($res)){
                ?>
                <tr>
                    <td><span class="badge bg-secondary"><?php echo $row['id']; ?></span></td>
                    <td><small class="fw-bold text-success"><?php echo $row['categoria']; ?></small></td>
                    <td><?php echo $row['pregunta']; ?></td>
                    <td><small class="text-muted"><?php echo substr($row['respuesta'], 0, 50); ?>...</small></td>
                    <td>
                        <a href="editar.php?id=<?php echo $row['id']; ?>&type=rtype" class="btn btn-sm btn-outline-primary"><i class="fa-solid fa-pen"></i></a>
                        <button onclick="confirmarBorrado(<?php echo $row['id']; ?>, 'rtype')" class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-trash"></i></button>
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
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script> <script>
    $(document).ready(function () {
        // Inicializar DataTables en español
        var opciones = {
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json"
            },
            "pageLength": 10,
            "order": [[ 0, "desc" ]] // Ordenar por ID descendente
        };
        $('#tablaTest').DataTable(opciones);
        $('#tablaRel').DataTable(opciones);
    });

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
                // Llamada AJAX para borrar
                $.post('logic/delete.php', {id: id, type: type}, function(response) {
                    if(response.trim() == 'success') {
                        Swal.fire('¡Borrado!', 'La pregunta ha sido eliminada.', 'success')
                        .then(() => location.reload()); // Recargar página para actualizar tabla
                    } else {
                        Swal.fire('Error', 'Hubo un problema al borrar: ' + response, 'error');
                    }
                });
            }
        })
    }
</script>

<?php include 'includes/footer.php'; ?>
