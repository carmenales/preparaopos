<?php include 'includes/header.php'; ?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark mb-1">Exámenes Oficiales</h2>
        <p class="text-secondary small mb-0">Histórico de convocatorias agrupadas por año.</p>
    </div>
</div>

<?php
// 1. Obtener todos los cuestionarios
$sql = "SELECT distinct categoria FROM ptype WHERE categoria LIKE '%CUESTIONARIO%' ORDER BY categoria DESC";
$result = mysqli_query($link, $sql);

$examenesPorAnio = [];

if(mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        $catOriginal = $row['categoria'];
        
        // 2. Extraer AÑO y NOMBRE LIMPIO
        $anio = "Otros";
        
        // Regex para años 20XX o 19XX
        if (preg_match('/(20[0-9]{2}|19[0-9]{2})/', $catOriginal, $coincidencias)) {
            $anio = $coincidencias[0]; 
        } 
        // Regex para años de 2 dígitos (ej: 15, 18, 19) aislados
        elseif (preg_match('/\b([0-9]{2})\b/', $catOriginal, $coincidencias)) {
            $anio = "20" . $coincidencias[0]; 
        }

        // Limpiamos el nombre para dejar solo la variante (Ej: "Turno Libre", "Supuesto")
        $nombreExamen = str_ireplace("CUESTIONARIO", "", $catOriginal);
        $nombreExamen = str_replace($anio, "", $nombreExamen); // Quitamos el año completo
        $nombreExamen = str_replace(substr($anio, 2), "", $nombreExamen); // Quitamos el año corto
        $nombreExamen = trim($nombreExamen, " -_"); 
        
        // Si tras limpiar queda vacío, poner nombre genérico
        if(empty($nombreExamen) || strlen($nombreExamen) < 2) $nombreExamen = "General";

        // 3. Agrupar
        $examenesPorAnio[$anio][] = [
            'titulo' => strtoupper($nombreExamen),
            'full_cat' => $catOriginal
        ];
    }
    
    // Ordenar años de más reciente a más antiguo
    krsort($examenesPorAnio);

} else {
    echo '<div class="alert alert-warning">No hay exámenes cargados.</div>';
}
?>

<div class="row g-4">
    <?php foreach ($examenesPorAnio as $anio => $listaExamenes): ?>
        
        <div class="col-md-6 col-xl-4">
            <div class="card h-100 shadow-sm border-0 year-card">
                
                <div class="card-header border-0 bg-transparent pt-4 px-4 d-flex align-items-center">
                    <div class="rounded-3 bg-danger bg-opacity-10 text-danger p-2 me-3 text-center" style="min-width: 50px;">
                        <i class="fa-solid fa-calendar-days fs-4"></i>
                    </div>
                    <div>
                        <h4 class="fw-bold text-dark mb-0"><?php echo $anio; ?></h4>
                        <span class="text-muted small"><?php echo count($listaExamenes); ?> convocatorias</span>
                    </div>
                </div>

                <div class="card-body px-4 pb-4">
                    <hr class="text-muted opacity-25 mt-0 mb-3">
                    
                    <div class="d-flex flex-wrap gap-2">
                        <?php foreach ($listaExamenes as $ex): ?>
                            <a href="test.php?categoria=<?php echo urlencode($ex['full_cat']); ?>" 
                               class="btn btn-outline-secondary btn-sm rounded-pill px-3 py-2 flex-grow-1 text-truncate btn-opcion"
                               title="<?php echo $ex['titulo']; ?>">
                                <?php echo $ex['titulo']; ?>
                            </a>
                        <?php endforeach; ?>
                    </div>
                </div>

            </div>
        </div>

    <?php endforeach; ?>
</div>

<style>
/* Efecto hover suave para la tarjeta del año */
.year-card {
    transition: transform 0.2s, box-shadow 0.2s;
    background: #fff;
}
.year-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
}

/* Estilo de los botones de opciones */
.btn-opcion {
    border-color: #e2e8f0;
    color: #64748b;
    font-weight: 500;
    font-size: 0.85rem;
    transition: all 0.2s;
    background-color: #f8fafc;
}

.btn-opcion:hover {
    background-color: #fee2e2; /* Fondo rojo muy pálido */
    border-color: #ef4444;      /* Borde rojo */
    color: #b91c1c;             /* Texto rojo oscuro */
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.1);
}
</style>

<?php include 'includes/footer.php'; ?>
