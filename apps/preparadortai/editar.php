<?php
include 'includes/header.php';

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

// Validar parámetros
if (!isset($_GET['id']) || !isset($_GET['type'])) {
    echo "<div class='alert alert-danger m-4'>Faltan datos para editar.</div>";
    include 'includes/footer.php';
    exit;
}

$id = intval($_GET['id']);
$type = $_GET['type'];
$datos = null;
$incorrectas = [];

// Obtener datos actuales
if ($type == 'ptype') {
    $stmt = mysqli_prepare($link, "SELECT * FROM ptype WHERE id = ?");
    mysqli_stmt_bind_param($stmt, "i", $id);
    mysqli_stmt_execute($stmt);
    $res = mysqli_stmt_get_result($stmt);
    $datos = mysqli_fetch_assoc($res);
    mysqli_stmt_close($stmt);

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

$categories = [];
$currentCategoryFound = false;

$sqlCategories = "
    SELECT categoria
    FROM question_sets
    ORDER BY categoria
";
$resCategories = mysqli_query($link, $sqlCategories);

while ($row = mysqli_fetch_assoc($resCategories)) {
    if ($row['categoria'] === $datos['categoria']) {
        $currentCategoryFound = true;
    }

    $categories[] = $row['categoria'];
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
            <input type="hidden" name="type" value="<?php echo safe_text($type); ?>">
            <input type="hidden" name="categoria" id="categoria" value="<?php echo safe_text($datos['categoria']); ?>">

            <div class="mb-3">
                <span class="badge <?php echo ($type=='ptype')?'bg-primary':'bg-success'; ?> fs-6">
                    <?php echo ($type=='ptype')?'Tipo Test':'Relacionar'; ?>
                </span>
            </div>

            <div class="row g-3">
                <div class="col-md-4">
                    <label for="categoria_select" class="form-label">Categoría</label>
                    <select class="form-select" id="categoria_select" required>
                        <?php foreach ($categories as $category): ?>
                            <option value="<?php echo safe_text($category); ?>" <?php echo $datos['categoria'] === $category ? 'selected' : ''; ?>>
                                <?php echo safe_text($category); ?>
                            </option>
                        <?php endforeach; ?>
                        <option value="__new__" <?php echo !$currentCategoryFound ? 'selected' : ''; ?>>+ Nueva categoría manual</option>
                    </select>

                    <input type="text"
                           class="form-control mt-2 <?php echo $currentCategoryFound ? 'd-none' : ''; ?>"
                           id="categoria_nueva"
                           value="<?php echo !$currentCategoryFound ? safe_text($datos['categoria']) : ''; ?>"
                           placeholder="Nueva categoría">

                    <div class="form-text">
                        Seleccionar una categoría existente evita duplicados.
                    </div>
                </div>

                <div class="col-md-4">
                    <label class="form-label">Bloque</label>
                    <input type="number" class="form-control" name="bloque" value="<?php echo safe_text($datos['bloque']); ?>">
                </div>
                <div class="col-md-4">
                    <label class="form-label">Tema</label>
                    <input type="number" class="form-control" name="tema" value="<?php echo safe_text($datos['tema']); ?>">
                </div>
            </div>

            <hr class="my-4">

            <div class="mb-3">
                <label class="form-label fw-bold">Pregunta</label>
                <textarea class="form-control" name="pregunta" rows="2" required><?php echo safe_text($datos['pregunta']); ?></textarea>
            </div>

            <div class="mb-3">
                <label class="form-label fw-bold text-success">Respuesta Correcta</label>
                <input type="text" class="form-control border-success" name="correcta" value="<?php echo safe_text($datos['respuesta']); ?>" required>
            </div>

            <?php if ($type == 'ptype'): ?>
                <div class="mb-4">
                    <label class="form-label">Justificación General</label>
                    <textarea class="form-control bg-light" name="justificacion" rows="2"><?php echo safe_text($datos['justif'] ?? ''); ?></textarea>
                </div>

                <div class="p-3 border rounded bg-light mt-4">
                    <label class="form-label fw-bold text-danger mb-3">Opciones Incorrectas</label>
                    <div class="field_wrapper">
                        <?php
                        foreach($incorrectas as $inc) {
                        ?>
                        <div class="row g-2 mb-2 input-group-row">
                            <div class="col-md-6">
                                <input type="text" name="field_name[]" class="form-control" value="<?php echo safe_text($inc['respuesta']); ?>">
                            </div>
                            <div class="col-md-5">
                                <input type="text" name="justif_name[]" class="form-control" value="<?php echo safe_text($inc['justif']); ?>" placeholder="Justificación">
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
    var wrapper = $('.field_wrapper');
    var addButton = $('.add_button');

    var fieldHTML = `
        <div class="row g-2 mb-2 input-group-row border-top pt-2">
            <div class="col-md-6"><input type="text" name="field_name[]" class="form-control" placeholder="Nueva Incorrecta"></div>
            <div class="col-md-5"><input type="text" name="justif_name[]" class="form-control" placeholder="Justificación"></div>
            <div class="col-md-1 d-grid"><button type="button" class="btn btn-outline-danger remove_button"><i class="fa-solid fa-trash"></i></button></div>
        </div>`;

    $(addButton).click(function(){
        $(wrapper).find('.row:last').before(fieldHTML);
    });

    $(wrapper).on('click', '.remove_button', function(e){
        e.preventDefault();
        $(this).closest('.input-group-row').remove();
    });

    $("#categoria_select").change(function() {
        if ($(this).val() === "__new__") {
            $("#categoria_nueva").removeClass("d-none").focus();
        } else {
            $("#categoria_nueva").addClass("d-none").val("");
            $("#categoria").val($(this).val());
        }
    });

    $("#categoria_nueva").on("input", function() {
        updateCategoryInput();
    });

    updateCategoryInput();
});

function updateCategoryInput() {
    var selectedCategory = $("#categoria_select").val();

    if (selectedCategory === "__new__") {
        $("#categoria").val($("#categoria_nueva").val().trim());
    } else {
        $("#categoria").val(selectedCategory);
    }
}

function updateData() {
    updateCategoryInput();

    if ($("#categoria").val() === "") {
        $('#msgResult').html('<div class="alert alert-danger">La categoría es obligatoria.</div>');
        return;
    }

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
