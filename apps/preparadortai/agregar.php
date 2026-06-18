<?php
include 'includes/header.php';

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

$selectedCategory = trim((string)($_GET['categoria'] ?? ''));

$categories = [];
$sqlCategories = "
    SELECT categoria
    FROM question_sets
    ORDER BY categoria
";
$resCategories = mysqli_query($link, $sqlCategories);

while ($row = mysqli_fetch_assoc($resCategories)) {
    $categories[] = $row['categoria'];
}

$selectedCategoryExists = in_array($selectedCategory, $categories, true);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold"><i class="fa-solid fa-plus-circle"></i> Añadir Nueva Pregunta</h2>
    <a href="gestionar.php" class="btn btn-outline-secondary btn-sm"><i class="fa-solid fa-arrow-left"></i> Volver</a>
</div>

<?php if (isset($_GET['created_category']) && $selectedCategory !== ''): ?>
    <div class="alert alert-success">
        Categoría creada correctamente. Ya puedes añadir preguntas a <strong><?php echo safe_text($selectedCategory); ?></strong>.
    </div>
<?php endif; ?>

<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="card shadow-sm border-0">
            <div class="card-body p-4">

                <form id="addform" method="post" class="needs-validation">

                    <div class="mb-4 p-3 bg-light rounded border">
                        <label class="form-label fw-bold d-block">Tipo de Ejercicio:</label>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="type" id="ptype" value="ptype" checked>
                            <label class="form-check-label" for="ptype"><i class="fa-solid fa-list-ul"></i> Test (Pregunta + Opciones)</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="type" id="rtype" value="rtype">
                            <label class="form-check-label" for="rtype"><i class="fa-solid fa-arrows-left-right"></i> Relacionar (Concepto + Definición)</label>
                        </div>
                    </div>

                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="d-flex justify-content-between align-items-center">
                                <label for="categoria_select" class="form-label">Categoría</label>
                                <a href="nueva_categoria.php" class="small text-decoration-none">
                                    <i class="fa-solid fa-folder-plus"></i> Nueva
                                </a>
                            </div>

                            <select class="form-select" id="categoria_select" required>
                                <option value="">Selecciona una categoría...</option>
                                <?php foreach ($categories as $category): ?>
                                    <option value="<?php echo safe_text($category); ?>" <?php echo $selectedCategory === $category ? 'selected' : ''; ?>>
                                        <?php echo safe_text($category); ?>
                                    </option>
                                <?php endforeach; ?>
                                <option value="__new__" <?php echo ($selectedCategory !== '' && !$selectedCategoryExists) ? 'selected' : ''; ?>>+ Nueva categoría manual</option>
                            </select>

                            <input type="text"
                                   class="form-control mt-2 <?php echo ($selectedCategory !== '' && !$selectedCategoryExists) ? '' : 'd-none'; ?>"
                                   id="categoria_nueva"
                                   value="<?php echo ($selectedCategory !== '' && !$selectedCategoryExists) ? safe_text($selectedCategory) : ''; ?>"
                                   placeholder="Nueva categoría">

                            <div class="form-text">
                                Seleccionar una categoría existente evita duplicados.
                            </div>
                        </div>

                        <div class="col-md-4">
                            <label for="bloque" class="form-label">Bloque (Número)</label>
                            <input type="number" class="form-control" id="bloque" name="bloque">
                        </div>
                        <div class="col-md-4">
                            <label for="tema" class="form-label">Tema (Número)</label>
                            <input type="number" class="form-control" id="tema" name="tema">
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="mb-3">
                        <label for="pregunta" class="form-label fw-bold">Enunciado / Pregunta</label>
                        <textarea class="form-control" id="pregunta" name="pregunta" rows="2" required></textarea>
                    </div>

                    <div class="mb-3">
                        <label for="correcta" class="form-label fw-bold text-success">Respuesta Correcta</label>
                        <div class="input-group">
                            <span class="input-group-text bg-success text-white"><i class="fa-solid fa-check"></i></span>
                            <input type="text" class="form-control border-success" id="correcta" name="correcta" required>
                        </div>
                    </div>

                    <div id="div-justificacion-general" class="mb-4">
                        <label for="justificacion" class="form-label">Justificación (Opcional)</label>
                        <textarea class="form-control bg-light" id="justificacion" name="justificacion" rows="2" placeholder="Explicación de por qué es correcta..."></textarea>
                    </div>

                    <div id="respuestas-incorrectas" class="p-3 border rounded bg-light mt-4">
                        <label class="form-label fw-bold text-danger mb-3">Opciones Incorrectas (Distractores)</label>

                        <div class="field_wrapper">
                            <div class="row g-2 mb-2 input-group-row">
                                <div class="col-md-6">
                                    <input type="text" name="field_name[]" class="form-control" placeholder="Respuesta Incorrecta 1" required>
                                </div>
                                <div class="col-md-5">
                                    <input type="text" name="justif_name[]" class="form-control" placeholder="Justificación (Opcional)">
                                </div>
                                <div class="col-md-1"></div>
                            </div>
                            <div class="row g-2 mb-2 input-group-row">
                                <div class="col-md-6">
                                    <input type="text" name="field_name[]" class="form-control" placeholder="Respuesta Incorrecta 2" required>
                                </div>
                                <div class="col-md-5">
                                    <input type="text" name="justif_name[]" class="form-control" placeholder="Justificación (Opcional)">
                                </div>
                                <div class="col-md-1"></div>
                            </div>
                            <div class="row g-2 mb-2 input-group-row">
                                <div class="col-md-6">
                                    <input type="text" name="field_name[]" class="form-control" placeholder="Respuesta Incorrecta 3" required>
                                </div>
                                <div class="col-md-5">
                                    <input type="text" name="justif_name[]" class="form-control" placeholder="Justificación (Opcional)">
                                </div>
                                <div class="col-md-1 d-grid">
                                    <button type="button" class="btn btn-success add_button" title="Añadir otra opción"><i class="fa-solid fa-plus"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="d-grid gap-2 mt-4">
                        <button type="button" class="btn btn-primary btn-lg" onclick="SubmitFormData()">
                            <i class="fa-solid fa-save"></i> Guardar Pregunta
                        </button>
                    </div>

                    <div id="results" class="mt-3"></div>

                </form>
            </div>
        </div>
    </div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<script>
$(document).ready(function() {
    var maxField = 10;
    var addButton = $('.add_button');
    var wrapper = $('.field_wrapper');
    var x = 3;

    var fieldHTML = `
        <div class="row g-2 mb-2 input-group-row border-top pt-2">
            <div class="col-md-6">
                <input type="text" name="field_name[]" class="form-control" placeholder="Otra Respuesta Incorrecta">
            </div>
            <div class="col-md-5">
                <input type="text" name="justif_name[]" class="form-control" placeholder="Justificación">
            </div>
            <div class="col-md-1 d-grid">
                <button type="button" class="btn btn-outline-danger remove_button"><i class="fa-solid fa-trash"></i></button>
            </div>
        </div>`;

    $(addButton).click(function() {
        if (x < maxField) {
            x++;
            $(wrapper).append(fieldHTML);
        }
    });

    $(wrapper).on('click', '.remove_button', function(e) {
        e.preventDefault();
        $(this).closest('.input-group-row').remove();
        x--;
    });

    $("#rtype").click(function() {
        $("#respuestas-incorrectas").slideUp();
        $("#div-justificacion-general").slideUp();
        $("input[name='field_name[]']").val("");
        $("input[name='justif_name[]']").val("");
    });

    $("#ptype").click(function() {
        $("#respuestas-incorrectas").slideDown();
        $("#div-justificacion-general").slideDown();
    });

    $("#categoria_select").change(function() {
        if ($(this).val() === "__new__") {
            $("#categoria_nueva").removeClass("d-none").prop("required", true).focus();
        } else {
            $("#categoria_nueva").addClass("d-none").prop("required", false).val("");
        }
    });
});

function getCategoriaValue() {
    var selectedCategory = $("#categoria_select").val();

    if (selectedCategory === "__new__") {
        return $("#categoria_nueva").val().trim();
    }

    return selectedCategory;
}

function SubmitFormData() {
    var formData = {
        bloque: $("#bloque").val(),
        tema: $("#tema").val(),
        categoria: getCategoriaValue(),
        type: $("input[name='type']:checked").val(),
        pregunta: $("#pregunta").val(),
        correcta: $("#correcta").val(),
        justificacion: $("#justificacion").val(),
        incorrectas: $("input[name='field_name[]']").map(function(){return $(this).val();}).get(),
        justif: $("input[name='justif_name[]']").map(function(){return $(this).val();}).get()
    };

    if(formData.pregunta === "" || formData.correcta === "" || formData.categoria === "") {
        alert("Por favor completa los campos obligatorios (Categoría, Pregunta, Respuesta Correcta)");
        return;
    }

    $.post("logic/submit.php", formData, function(data) {
        $('#results').show().html('<div class="alert alert-success mt-3"><i class="fa-solid fa-check-circle"></i> ' + data + '</div>');
        limpia();
        setTimeout(function(){ $('#results').fadeOut(); }, 5000);
    }).fail(function() {
        $('#results').html('<div class="alert alert-danger mt-3">Error al guardar. Verifica la consola.</div>');
    });
}

function limpia() {
    $("#pregunta").val("");
    $("#correcta").val("");
    $("#justificacion").val("");
    $("input[name='field_name[]']").val("");
    $("input[name='justif_name[]']").val("");
}
</script>

<?php include 'includes/footer.php'; ?>
