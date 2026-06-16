<?php include 'includes/header.php'; ?>

<div class="row justify-content-center">
    <div class="col-lg-8">
        
        <div class="text-center mb-5">
            <h1 class="fw-bold text-dark">Changelog</h1>
            <p class="text-secondary">Evolución del proyecto Preparador TAI</p>
            <span class="badge bg-primary rounded-pill px-3 py-2">Versión Actual: v2.0</span>
        </div>

        <div class="border-start border-2 border-primary ms-3 ps-4 position-relative">
            
            <div class="mb-5 position-relative">
                <div class="position-absolute top-0 start-0 translate-middle ms-n4 bg-primary rounded-circle border border-4 border-white" style="width: 20px; height: 20px;"></div>
                <h3 class="fw-bold text-primary">v2.0 - Actualización</h3>
                <span class="text-muted small"><i class="fa-regular fa-calendar me-1"></i> 20 Diciembre 2025</span>
                
                <div class="card shadow-sm mt-3 border-0">
                    <div class="card-body">
                        <h6 class="fw-bold"><i class="fa-solid fa-paintbrush text-success"></i> Rediseño Visual</h6>
                        <ul class="mb-3 text-secondary small">
                            <li>Implementación de <strong>Bootstrap 5</strong> para diseño responsivo.</li>
                            <li>Nuevo Sidebar oscuro "Enterprise" con categorías y submenús.</li>
                            <li>Iconografía moderna con FontAwesome 6.</li>
                            <li>Efectos visuales en tarjetas y botones (Hover, transiciones).</li>
                        </ul>

                        <h6 class="fw-bold"><i class="fa-solid fa-code text-danger"></i> Backend & Estructura</h6>
                        <ul class="mb-3 text-secondary small">
                            <li>Separación de código MVC: <code>includes/</code>, <code>logic/</code>, <code>assets/</code>.</li>
                            <li>Unificación de vistas: <code>index.php</code> (Dashboard), <code>temas.php</code>, <code>practica.php</code>.</li>
                            <li>Optimización de consultas SQL y eliminación de archivos redundantes.</li>
                        </ul>

                        <h6 class="fw-bold"><i class="fa-solid fa-wand-magic-sparkles text-warning"></i> Nuevas Funcionalidades</h6>
                        <ul class="mb-0 text-secondary small">
                            <li><strong>Gestor CRUD con DataTables:</strong> Búsqueda, ordenación y paginación instantánea.</li>
                            <li><strong>Sistema de Edición:</strong> Modificar preguntas y respuestas incorrectas desde interfaz.</li>
                            <li><strong>Borrado Seguro:</strong> Alertas con SweetAlert2 para evitar accidentes.</li>
                            <li>Feedback visual interactivo al responder preguntas (Verde/Rojo) sin recargar.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="mb-5 position-relative">
                <div class="position-absolute top-0 start-0 translate-middle ms-n4 bg-secondary rounded-circle border border-4 border-white" style="width: 20px; height: 20px;"></div>
                <h3 class="fw-bold text-secondary">v1.0 - Origen</h3>
                <span class="text-muted small"><i class="fa-regular fa-calendar me-1"></i> Versión Inicial</span>
                
                <div class="card shadow-sm mt-3 border-0 bg-light">
                    <div class="card-body">
                        <ul class="mb-0 text-secondary small">
                            <li>Script básico en PHP plano.</li>
                            <li>Funcionalidad principal: Tests aleatorios (ptype) y Relacionar (rtype).</li>
                            <li>Interfaz básica HTML/CSS sin frameworks.</li>
                            <li>Añadido manual de preguntas.</li>
                        </ul>
                    </div>
                </div>
            </div>

        </div> </div>
</div>

<?php include 'includes/footer.php'; ?>
