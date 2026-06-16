<?php 
include 'includes/header.php'; 

// Validar parámetros
if (!isset($_GET['id']) || !isset($_GET['type'])) {
    echo "<div class='alert alert-danger m-4'>Faltan datos para editar.</div>";
    include 'includes/footer.php';
    exit;
}

$id = intval($_GET['id']);
$type = $_GET['type']; // 'ptype' o 'rtype'
$datos = null;
$incorrectas = [];

// Obtener datos actuales
if ($type == 'ptype') {
    // 1. Datos principales
    $stmt = mysqli_prepare($link, "SELECT * FROM ptype WHERE id = ?");
    mysqli_stmt_bind_param($stmt, "i", $id);
    mysqli_stmt_execute($stmt);
    $res = mysqli_stmt_get_result($stmt);
    $datos = mysqli_fetch_assoc($res);
    mysqli_stmt_close($stmt);

    // 2. Respuestas incorrectas
    $stmt2 = mysqli_prepare($link, "SELECT * FROM incorrectas WHERE id_pregunta = ?");
    mysqli_stmt_bind_param($stmt2, "i", $id);
    mysqli_stmt_execute($stmt2);
    $res2 = mysqli_stmt_get_result($stmt2);
    while($row = mysqli_fetch_assoc($res2)) {
        $incorrectas[] = $row;
    }
    mysqli_stmt_close($stmt2);

} elseif ($type == 'rtype') {
    $stmt = mysqli_prepare($link, "SELECT * FROM rtype WHERE id = ?");
    mysqli_stmt_bind_param($stmt, "i", $id);
    mysqli_stmt_execute($stmt);
    $res = mysqli_stmt_get_result($stmt);
    $datos = mysqli_fetch_assoc($res);
    mysqli_stmt_close($stmt);
}

if (!$datos) {
    echo "<div class='alert alert-danger m-4'>Pregunta no encontrada.</div>";
    include 'includes/footer.php';
    exit;
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold"><i class="fa-solid fa-pen-to-square"></i> Editar Pregunta #<?php echo $id; ?></h2>
    <a href="gestionar.php" class="btn btn-outline-secondary btn-sm"><i class="fa-solid fa-arrow-left"></i> Cancelar</a>
</div>

<div class="card shadow-sm border-0">
    <div class="card-body p-4">
        
        <form id="editForm" class="needs-validation">
            <input type="hidden" name="id" value="<?php echo $id; ?>">
            <input type="hidden" name="type" value="<?php echo $type; ?>">

            <div class="mb-3">
                <span class="badge <?php echo ($type=='ptype')?'bg-primary':'bg-success'; ?> fs-6">
                    <?php echo ($type=='ptype')?'Tipo Test':'Relacionar'; ?>
                </span>
            </div>

            <div class="row g-3">
                <div class="col-md-4">
                    <label class="form-label">Categoría</label>
                    <input type="text" class="form-control" name="categoria" value="<?php echo htmlspecialchars($datos['categoria']); ?>" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Bloque</label>
                    <input type="number" class="form-control" name="bloque" value="<?php echo htmlspecialchars($datos['bloque']); ?>">
                </div>
                <div class="col-md-4">
                    <label class="form-label">Tema</label>
                    <input type="number" class="form-control" name="tema" value="<?php echo htmlspecialchars($datos['tema']); ?>">
                </div>
            </div>

            <hr class="my-4">

            <div class="mb-3">
                <label class="form-label fw-bold">Pregunta</label>
                <textarea class="form-control" name="pregunta" rows="2" required><?php echo htmlspecialchars($datos['pregunta']); ?></textarea>
            </div>

            <div class="mb-3">
                <label class="form-label fw-bold text-success">Respuesta Correcta</label>
                <input type="text" class="form-control border-success" name="correcta" value="<?php echo htmlspecialchars($datos['respuesta']); ?>" required>
            </div>

            <?php if ($type == 'ptype'): ?>
                <div class="mb-4">
                    <label class="form-label">Justificación General</label>
                    <textarea class="form-control bg-light" name="justificacion" rows="2"><?php echo htmlspecialchars($datos['justif'] ?? ''); ?></textarea>
                </div>

                <div class="p-3 border rounded bg-light mt-4">
                    <label class="form-label fw-bold text-danger mb-3">Opciones Incorrectas</label>
                    <div class="field_wrapper">
                        <?php 
                        foreach($incorrectas as $inc) { 
                        ?>
                        <div class="row g-2 mb-2 input-group-row">
                            <div class="col-md-6">
                                <input type="text" name="field_name[]" class="form-control" value="<?php echo htmlspecialchars($inc['respuesta']); ?>">
                            </div>
                            <div class="col-md-5">
                                <input type="text" name="justif_name[]" class="form-control" value="<?php echo htmlspecialchars($inc['justif']); ?>" placeholder="Justificación">
                            </div>
                            <div class="col-md-1 d-grid">
                                <button type="button" class="btn btn-outline-danger remove_button"><i class="fa-solid fa-trash"></i></button>
                            </div>
                        </div>
                        <?php } ?>
                        
                        <div class="row g-2 mb-2">
                             <div class="col-12 text-end">
                                <button type="button" class="btn btn-success btn-sm add_button"><i class="fa-solid fa-plus"></i> Añadir Opción</button>
                             </div>
                         </div>
                    </div>
                </div>
            <?php endif; ?>

            <div class="d-grid gap-2 mt-4">
                <button type="button" class="btn btn-primary btn-lg" onclick="updateData()">
                    <i class="fa-solid fa-floppy-disk"></i> Guardar Cambios
                </button>
            </div>
            
            <div id="msgResult" class="mt-3"></div>

        </form>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
$(document).ready(function() {
    // Lógica para añadir/quitar campos (igual que en agregar.php)
    var wrapper = $('.field_wrapper'); 
    var addButton = $('.add_button');
    
    var fieldHTML = `
        <div class="row g-2 mb-2 input-group-row border-top pt-2">
            <div class="col-md-6"><input type="text" name="field_name[]" class="form-control" placeholder="Nueva Incorrecta"></div>
            <div class="col-md-5"><input type="text" name="justif_name[]" class="form-control" placeholder="Justificación"></div>
            <div class="col-md-1 d-grid"><button type="button" class="btn btn-outline-danger remove_button"><i class="fa-solid fa-trash"></i></button></div>
        </div>`;

    $(addButton).click(function(){
        $(wrapper).find('.row:last').before(fieldHTML); // Insertar antes del botón de añadir
    });

    $(wrapper).on('click', '.remove_button', function(e){
        e.preventDefault();
        $(this).closest('.input-group-row').remove();
    });
});

function updateData() {
    var formData = $('#editForm').serialize();
    
    $.post('logic/update.php', formData, function(response) {
        if(response.trim() === 'success') {
            $('#msgResult').html('<div class="alert alert-success">¡Guardado correctamente! Redirigiendo...</div>');
            setTimeout(function(){ window.location.href = 'gestionar.php'; }, 1500);
        } else {
            $('#msgResult').html('<div class="alert alert-danger">Error: ' + response + '</div>');
        }
    }).fail(function() {
        $('#msgResult').html('<div class="alert alert-danger">Error de conexión.</div>');
    });
}
</script>

<?php include 'includes/footer.php'; ?>
