<?php
include 'includes/header.php';

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

$questionSetId = isset($_GET['id']) ? (int)$_GET['id'] : 0;

if ($questionSetId <= 0) {
    ?>
    <div class="alert alert-danger shadow-sm border-0">
        Categoría no válida.
    </div>

    <a href="categorias.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a categorías
    </a>
    <?php
    include 'includes/footer.php';
    exit;
}

$sql = "
    SELECT
        id,
        categoria,
        organismo,
        proceso_selectivo,
        convocatoria_year,
        turno,
        tipo,
        descripcion
    FROM question_sets
    WHERE id = ?
";

$stmt = mysqli_prepare($link, $sql);
mysqli_stmt_bind_param($stmt, "i", $questionSetId);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);
$questionSet = mysqli_fetch_assoc($result);
mysqli_stmt_close($stmt);

if (!$questionSet) {
    ?>
    <div class="alert alert-warning shadow-sm border-0">
        No se ha encontrado la categoría.
    </div>

    <a href="categorias.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a categorías
    </a>
    <?php
    include 'includes/footer.php';
    exit;
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-pen-to-square"></i> Editar categoría
    </h2>

    <a href="categorias.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver
    </a>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-tags text-primary"></i> Datos de la categoría
        </h5>
    </div>

    <div class="card-body">
        <form method="post" action="logic/update_question_set.php">
            <input type="hidden" name="id" value="<?php echo (int)$questionSet['id']; ?>">
            <input type="hidden" name="old_categoria" value="<?php echo safe_text($questionSet['categoria']); ?>">

            <div class="mb-3">
                <label for="categoria" class="form-label">Categoría</label>
                <input type="text"
                       id="categoria"
                       name="categoria"
                       class="form-control"
                       value="<?php echo safe_text($questionSet['categoria']); ?>"
                       required>
                <div class="form-text">
                    Si cambias este valor, se actualizará también en las preguntas y sesiones asociadas.
                    No se permite usar una categoría que ya exista.
                </div>
            </div>

            <div class="row g-3">
                <div class="col-md-4">
                    <label for="organismo" class="form-label">Organismo</label>
                    <input type="text"
                           id="organismo"
                           name="organismo"
                           class="form-control"
                           list="organismo-options"
                           value="<?php echo safe_text($questionSet['organismo']); ?>"
                           placeholder="AGE, UPM, Ayuntamiento Madrid...">
                    <datalist id="organismo-options">
                        <option value="AGE">
                        <option value="UPM">
                        <option value="Ayuntamiento Madrid">
                        <option value="Comunidad de Madrid">
                    </datalist>
                </div>

                <div class="col-md-4">
                    <label for="proceso_selectivo" class="form-label">Proceso selectivo</label>
                    <input type="text"
                           id="proceso_selectivo"
                           name="proceso_selectivo"
                           class="form-control"
                           list="proceso-options"
                           value="<?php echo safe_text($questionSet['proceso_selectivo']); ?>"
                           placeholder="TAI, GSI, TIC Superior...">
                    <datalist id="proceso-options">
                        <option value="TAI">
                        <option value="GSI">
                        <option value="TIC Superior">
                        <option value="Técnico Gestión STI">
                        <option value="Auxiliar TIC">
                    </datalist>
                </div>

                <div class="col-md-4">
                    <label for="convocatoria_year" class="form-label">Año convocatoria</label>
                    <input type="number"
                           id="convocatoria_year"
                           name="convocatoria_year"
                           class="form-control"
                           min="2000"
                           max="2100"
                           value="<?php echo safe_text($questionSet['convocatoria_year']); ?>"
                           placeholder="2024">
                </div>

                <div class="col-md-4">
                    <label for="turno" class="form-label">Turno</label>
                    <input type="text"
                           id="turno"
                           name="turno"
                           class="form-control"
                           list="turno-options"
                           value="<?php echo safe_text($questionSet['turno']); ?>"
                           placeholder="Libre, Promocion interna...">
                    <datalist id="turno-options">
                        <option value="Libre">
                        <option value="Promocion interna">
                        <option value="Discapacidad">
                    </datalist>
                </div>

                <div class="col-md-4">
                    <label for="tipo" class="form-label">Tipo</label>
                    <input type="text"
                           id="tipo"
                           name="tipo"
                           class="form-control"
                           list="tipo-options"
                           value="<?php echo safe_text($questionSet['tipo']); ?>"
                           placeholder="Examen oficial, Test tematico...">
                    <datalist id="tipo-options">
                        <option value="Examen oficial">
                        <option value="Test tematico">
                        <option value="Supuesto practico">
                        <option value="Simulacro">
                    </datalist>
                </div>

                <div class="col-md-12">
                    <label for="descripcion" class="form-label">Descripción</label>
                    <textarea id="descripcion"
                              name="descripcion"
                              class="form-control"
                              rows="3"
                              placeholder="Notas internas sobre esta categoría"><?php echo safe_text($questionSet['descripcion']); ?></textarea>
                </div>
            </div>

            <div class="d-flex justify-content-end gap-2 mt-4">
                <a href="categorias.php" class="btn btn-outline-secondary">
                    Cancelar
                </a>

                <button type="submit" class="btn btn-primary">
                    <i class="fa-solid fa-floppy-disk"></i> Guardar cambios
                </button>
            </div>
        </form>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
