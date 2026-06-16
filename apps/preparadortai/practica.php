<?php include 'includes/header.php'; ?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1">Ejercicios de Práctica</h2>
        <p class="text-secondary small mb-0">Relaciona conceptos con sus definiciones correspondientes.</p>
    </div>
</div>

<div class="row g-4">
    <?php
    // Categorías de la tabla rtype
    $sql = "SELECT distinct categoria FROM rtype ORDER BY categoria ASC";
    $result = mysqli_query($link, $sql);
    
    if(mysqli_num_rows($result) > 0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $cat = $row['categoria'];
    ?>
        <div class="col-md-6 col-xl-4">
            <div class="card h-100 shadow-sm hover-card border-0" style="background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%);">
                <div class="card-body position-relative overflow-hidden">
                    <div class="d-flex justify-content-between align-items-start mb-4">
                        <div class="rounded-circle bg-success bg-opacity-10 p-3 text-success">
                            <i class="fa-solid fa-puzzle-piece fs-4"></i>
                        </div>
                    </div>
                    
                    <h5 class="card-title fw-bold text-dark"><?php echo $cat; ?></h5>
                    <p class="text-muted small mb-4">Arrastra o selecciona las parejas correctas.</p>
                    
                    <a href="relacionar.php?categoria=<?php echo urlencode($cat); ?>" class="btn btn-outline-success w-100 rounded-pill stretched-link">
                        Entrar <i class="fa-solid fa-play ms-2"></i>
                    </a>
                </div>
            </div>
        </div>
    <?php 
        }
    } else {
        echo '<div class="col-12"><div class="alert alert-info">No hay ejercicios de relacionar creados todavía.</div></div>';
    }
    ?>
</div>

<?php include 'includes/footer.php'; ?>
