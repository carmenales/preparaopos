<?php 
include 'includes/header.php'; 
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold"><i class="fa-solid fa-plus-circle"></i> Añadir Nueva Pregunta</h2>
    <a href="index.php" class="btn btn-outline-secondary btn-sm"><i class="fa-solid fa-arrow-left"></i> Volver</a>
</div>

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
                            <label for="categoria" class="form-label">Categoría</label>
                            <input list="categorias" class="form-control" name="categoria" id="categoria" placeholder="Escribe o selecciona..." required>
                            <datalist id="categorias">
                                <?php
                                // Cargamos las categorías existentes para ayudar al autocompletado
                                $sql = "SELECT DISTINCT categoria FROM rtype UNION SELECT DISTINCT categoria FROM ptype";
                                $stmt = mysqli_prepare($link, $sql);
                                mysqli_stmt_execute($stmt);
                                mysqli_stmt_bind_result($stmt, $catName);
                                while (mysqli_stmt_fetch($stmt)) {
                                    echo "<option value=\"$catName\">";
                                }
                                mysqli_stmt_close($stmt);
                                ?>
                            </datalist>
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
    var x = 3; // Empezamos con 3 campos

    // HTML para nuevos campos
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

    // Añadir campos
    $(addButton).click(function() {
        if (x < maxField) {
            x++;
            $(wrapper).append(fieldHTML);
        }
    });

    // Eliminar campos
    $(wrapper).on('click', '.remove_button', function(e) {
        e.preventDefault();
        $(this).closest('.input-group-row').remove();
        x--;
    });

    // Mostrar/Ocultar según tipo
    $("#rtype").click(function() {
        $("#respuestas-incorrectas").slideUp();
        $("#div-justificacion-general").slideUp();
        // Limpiar campos incorrectos para evitar envío de basura
        $("input[name='field_name[]']").val("");
        $("input[name='justif_name[]']").val("");
    });
    $("#ptype").click(function() {
        $("#respuestas-incorrectas").slideDown();
        $("#div-justificacion-general").slideDown();
    });
});

function SubmitFormData() {
    // Recoger valores
    var formData = {
        bloque: $("#bloque").val(),
        tema: $("#tema").val(),
        categoria: $("#categoria").val(),
        type: $("input[name='type']:checked").val(),
        pregunta: $("#pregunta").val(),
        correcta: $("#correcta").val(),
        justificacion: $("#justificacion").val(),
        incorrectas: $("input[name='field_name[]']").map(function(){return $(this).val();}).get(),
        justif: $("input[name='justif_name[]']").map(function(){return $(this).val();}).get()
    };

    // Validacion básica
    if(formData.pregunta === "" || formData.correcta === "" || formData.categoria === "") {
        alert("Por favor completa los campos obligatorios (Categoría, Pregunta, Respuesta Correcta)");
        return;
    }

    // AJAX POST a la carpeta LOGIC
    $.post("logic/submit.php", formData, function(data) {
        $('#results').html('<div class="alert alert-success mt-3"><i class="fa-solid fa-check-circle"></i> ' + data + '</div>');
        // Limpiar formulario si quieres
        limpia(); 
        // Desvanecer mensaje tras 3 segundos
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
    // No limpiamos categoría para facilitar meter varias seguidas
}
</script>

<?php include 'includes/footer.php'; ?>
