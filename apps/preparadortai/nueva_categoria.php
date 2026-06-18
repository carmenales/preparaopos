<?php
include 'includes/header.php';

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

$createdCategory = trim((string)($_GET['categoria'] ?? ''));
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="text-primary fw-bold mb-1"><i class="fa-solid fa-folder-plus"></i> Nueva Categoría</h2>
        <p class="text-secondary small mb-0">Crea una categoría para agrupar preguntas de un test, tema, bloque o proceso selectivo.</p>
    </div>

    <div class="d-flex gap-2">
        <a href="gestionar.php" class="btn btn-outline-secondary btn-sm"><i class="fa-solid fa-arrow-left"></i> Banco de Preguntas</a>
        <a href="agregar.php" class="btn btn-success btn-sm"><i class="fa-solid fa-plus"></i> Nueva Pregunta</a>
    </div>
</div>

<?php if (isset($_GET['created']) && $createdCategory !== ''): ?>
    <div class="alert alert-success">
        Categoría <strong><?php echo safe_text($createdCategory); ?></strong> creada correctamente.
        <a href="agregar.php?categoria=<?php echo urlencode($createdCategory); ?>" class="alert-link">Añadir preguntas</a>.
    </div>
<?php endif; ?>

<?php if (isset($_GET['error'])): ?>
    <?php if ($_GET['error'] === 'duplicate'): ?>
        <div class="alert alert-warning">
            Ya existe una categoría con ese nombre.
            <?php if ($createdCategory !== ''): ?>
                Puedes <a href="agregar.php?categoria=<?php echo urlencode($createdCategory); ?>" class="alert-link">añadir preguntas a esa categoría</a>.
            <?php endif; ?>
        </div>
    <?php elseif ($_GET['error'] === 'invalid_year'): ?>
        <div class="alert alert-danger">El año de convocatoria no es válido.</div>
    <?php else: ?>
        <div class="alert alert-danger">No se ha podido crear la categoría.</div>
    <?php endif; ?>
<?php endif; ?>

<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow-sm border-0">
            <div class="card-body p-4">

                <form method="post" action="logic/create_question_set.php" class="needs-validation">

                    <div class="mb-3">
                        <label for="categoria" class="form-label fw-bold">Categoría</label>
                        <input type="text"
                               class="form-control"
                               id="categoria"
                               name="categoria"
                               maxlength="255"
                               placeholder="Ej. CUESTIONARIO TAI 2024 - TAI-LI B2-B4"
                               required>
                        <div class="form-text">
                            Este es el valor que se guardará en las preguntas como categoría.
                        </div>
                    </div>

                    <div class="row g-3">
                        <div class="col-md-6">
                            <label for="organismo" class="form-label">Organismo</label>
                            <input type="text" class="form-control" id="organismo" name="organismo" maxlength="100" placeholder="Ej. AGE, UPM, Ayuntamiento de Madrid">
                        </div>

                        <div class="col-md-6">
                            <label for="proceso_selectivo" class="form-label">Proceso selectivo</label>
                            <input type="text" class="form-control" id="proceso_selectivo" name="proceso_selectivo" maxlength="150" placeholder="Ej. TAI, GSI, TIC Superior">
                        </div>

                        <div class="col-md-4">
                            <label for="convocatoria_year" class="form-label">Año</label>
                            <input type="number" class="form-control" id="convocatoria_year" name="convocatoria_year" min="1900" max="2100" placeholder="2024">
                        </div>

                        <div class="col-md-4">
                            <label for="turno" class="form-label">Turno</label>
                            <select class="form-select" id="turno" name="turno">
                                <option value="">Sin especificar</option>
                                <option value="Libre">Libre</option>
                                <option value="Promocion interna">Promocion interna</option>
                                <option value="Discapacidad">Discapacidad</option>
                                <option value="Estabilizacion">Estabilizacion</option>
                            </select>
                        </div>

                        <div class="col-md-4">
                            <label for="tipo" class="form-label">Tipo</label>
                            <select class="form-select" id="tipo" name="tipo">
                                <option value="">Sin especificar</option>
                                <option value="Examen oficial">Examen oficial</option>
                                <option value="Test tematico">Test tematico</option>
                                <option value="Simulacro">Simulacro</option>
                                <option value="Repaso">Repaso</option>
                            </select>
                        </div>
                    </div>

                    <div class="mt-3">
                        <label for="descripcion" class="form-label">Notas</label>
                        <textarea class="form-control"
                                  id="descripcion"
                                  name="descripcion"
                                  rows="3"
                                  maxlength="255"
                                  placeholder="Información útil para identificar esta categoría."></textarea>
                    </div>

                    <div class="d-flex justify-content-end gap-2 mt-4">
                        <button type="submit" name="next" value="stay" class="btn btn-outline-primary">
                            <i class="fa-solid fa-save"></i> Guardar
                        </button>

                        <button type="submit" name="next" value="add_questions" class="btn btn-success">
                            <i class="fa-solid fa-plus"></i> Guardar y añadir preguntas
                        </button>
                    </div>

                </form>
            </div>
        </div>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
