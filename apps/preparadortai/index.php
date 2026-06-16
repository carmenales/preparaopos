<?php 
include 'includes/header.php'; 

// Lógica original de contadores con tu variable $link
$sqlTotalTest = "SELECT COUNT(*) as total FROM ptype";
$resTest = mysqli_query($link, $sqlTotalTest);
$totalTest = mysqli_fetch_assoc($resTest)['total'];

$sqlTotalRel = "SELECT COUNT(*) as total FROM rtype";
$resRel = mysqli_query($link, $sqlTotalRel);
$totalRel = mysqli_fetch_assoc($resRel)['total'];

$totalPreguntas = $totalTest + $totalRel;
?>

<style>
    /* Fondo con textura de puntos para dar profundidad al gris de Bootstrap */
    #page-content-wrapper {
        background-color: #f8fafc !important;
        background-image: radial-gradient(#cbd5e1 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
    }

    /* Hero Section con degradado profesional */
    .hero-dashboard {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 24px;
        padding: 4rem 3rem;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
    }

    .hero-dashboard::after {
        content: "\f109"; /* Icono de laptop code */
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        position: absolute;
        right: -20px;
        bottom: -40px;
        font-size: 14rem;
        color: rgba(255, 255, 255, 0.05);
    }

    /* Tarjetas de navegación mejoradas */
    .nav-card-pro {
        border: none;
        border-radius: 20px;
        background: white;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        padding: 2.5rem 1.5rem;
    }

    .nav-card-pro:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15) !important;
    }

    .icon-wrapper {
        width: 70px;
        height: 70px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 1.8rem;
    }

    /* Esquema de colores para los iconos */
    .icon-blue { background: #e0f2fe; color: #0284c7; }
    .icon-green { background: #dcfce7; color: #16a34a; }
    .icon-amber { background: #fef3c7; color: #d97706; }

    .stat-badge {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-size: 0.9rem;
    }
</style>

<div class="container py-3">
    
    <div class="hero-dashboard shadow">
        <div class="row align-items-center">
            <div class="col-lg-8">
                <h1 class="display-5 fw-bold mb-3">Preparador TAI <span class="text-info">v2.0</span></h1>
                <p class="lead opacity-75 mb-0">Entrenamiento especializado para el Cuerpo de Técnicos Auxiliares de Informática de la Administración del Estado.</p>
            </div>
        </div>
    </div>

    <div class="row g-4 mb-5">
        <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 p-3 text-center border-bottom border-info border-4">
                <span class="text-muted small text-uppercase fw-bold">Banco de Preguntas</span>
                <h3 class="fw-bold m-0"><?php echo $totalPreguntas; ?></h3>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 p-3 text-center border-bottom border-primary border-4">
                <span class="text-muted small text-uppercase fw-bold">Nuevas Convocatorias</span>
                <h3 class="fw-bold m-0">2022 / 2024</h3>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 p-3 text-center border-bottom border-success border-4">
                <span class="text-muted small text-uppercase fw-bold">Examenes TAI</span>
                <h3 class="fw-bold m-0">Libre y PI</h3>
            </div>
        </div>
    </div>

    <div class="row g-4 justify-content-center">
        
        <div class="col-md-4">
            <a href="temas.php" class="text-decoration-none h-100 d-block">
                <div class="card nav-card-pro shadow-sm h-100">
                    <div class="icon-wrapper icon-blue">
                        <i class="fa-solid fa-book-open-reader"></i>
                    </div>
                    <h4 class="fw-bold text-dark">Repasar Temas</h4>
                    <p class="text-secondary small mb-0">Test varios para repasar temas.</p>
                </div>
            </a>
        </div>

        <div class="col-md-4">
            <a href="practica.php" class="text-decoration-none h-100 d-block">
                <div class="card nav-card-pro shadow-sm h-100">
                    <div class="icon-wrapper icon-green">
                        <i class="fa-solid fa-bolt-lightning"></i>
                    </div>
                    <h4 class="fw-bold text-dark">Práctica Rápida</h4>
                    <p class="text-secondary small mb-0">Test de repaso para practicar.</p>
                </div>
            </a>
        </div>

        <div class="col-md-4">
            <a href="examenes.php" class="text-decoration-none h-100 d-block">
                <div class="card nav-card-pro shadow-sm h-100">
                    <div class="icon-wrapper icon-amber">
                        <i class="fa-solid fa-file-signature"></i>
                    </div>
                    <h4 class="fw-bold text-dark">Cuestionarios</h4>
                    <p class="text-secondary small mb-0">Accede a los cuestionarios oficiales de las convocatorias 2014-2024.</p>
                </div>
            </a>
        </div>

    </div>

</div>

<?php include 'includes/footer.php'; ?>
