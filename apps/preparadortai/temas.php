<?php include 'includes/header.php'; ?>

<?php
function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

$sql = "
    SELECT
        p.categoria,
        COUNT(*) AS total_questions,
        qs.tipo
    FROM ptype p
    LEFT JOIN question_sets qs
        ON qs.categoria = p.categoria
    WHERE
        COALESCE(qs.tipo, '') <> 'Examen oficial'
        AND p.categoria NOT LIKE '%CUESTIONARIO%'
    GROUP BY
        p.categoria,
        qs.tipo
    ORDER BY p.categoria ASC
";

$result = mysqli_query($link, $sql);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1">Repasar Temas</h2>
        <p class="text-secondary small mb-0">Selecciona un bloque para realizar tests de repaso.</p>
    </div>
    <div class="d-none d-md-block">
        <div class="input-group">
            <span class="input-group-text bg-white border-end-0"><i class="fa-solid fa-magnifying-glass text-muted"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" placeholder="Buscar tema...">
        </div>
    </div>
</div>

<div class="row g-4">
    <?php if ($result && mysqli_num_rows($result) > 0): ?>
        <?php while ($row = mysqli_fetch_assoc($result)): ?>
            <?php $cat = $row['categoria']; ?>
            <div class="col-md-6 col-xl-4">
                <div class="card h-100 shadow-sm hover-card bg-white border-0">
                    <div class="card-body position-relative overflow-hidden">
                        <div class="d-flex justify-content-between align-items-start mb-4">
                            <div class="rounded-circle bg-primary bg-opacity-10 p-3 text-primary">
                                <i class="fa-solid fa-book fs-4"></i>
                            </div>
                            <span class="badge bg-light text-secondary border">
                                <?php echo (int)$row['total_questions']; ?> preguntas
                            </span>
                        </div>
                        <h5 class="card-title fw-bold text-dark"><?php echo safe_text($cat); ?></h5>
                        <p class="text-muted small mb-4">Preguntas teóricas y supuestos prácticos.</p>
                        <a href="test.php?categoria=<?php echo urlencode($cat); ?>" class="btn btn-outline-primary w-100 rounded-pill stretched-link">
                            Comenzar <i class="fa-solid fa-arrow-right ms-2"></i>
                        </a>
                    </div>
                </div>
            </div>
        <?php endwhile; ?>
    <?php else: ?>
        <div class="col-12">
            <div class="alert alert-warning">No hay temas de repaso disponibles. ¡Añade preguntas!</div>
        </div>
    <?php endif; ?>
</div>

<?php include 'includes/footer.php'; ?>
