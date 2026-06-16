<?php 
// Lógica para encontrar el archivo de configuración desde cualquier carpeta
if (file_exists('includes/config.php')) { 
    require_once 'includes/config.php'; 
} elseif (file_exists('../includes/config.php')) { 
    require_once '../includes/config.php'; 
} else { 
    // Fallback por si acaso
    require_once 'config.php'; 
}

// Detectar la página actual para marcar el menú como "activo"
$paginaActual = basename($_SERVER['PHP_SELF']);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preparador TAI v2.0</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

<div class="d-flex" id="wrapper">
    <div class="text-white border-end d-flex flex-column" id="sidebar-wrapper">
        
        <div class="sidebar-brand">
            <div class="d-flex align-items-center gap-2">
                <i class="fa-solid fa-graduation-cap fa-xl text-white"></i>
                <div>
                    <span class="brand-title">PREPARADOR TAI</span>
                    <span class="brand-version">v2.0</span>
                </div>
            </div>
        </div>
        
        <div class="list-group list-group-flush mt-2 flex-grow-1" style="overflow-y: auto; overflow-x: hidden;">
            
            <div class="sidebar-header">Zona de Estudio</div>
            
            <a href="index.php" class="list-group-item list-group-item-action list-group-item-dark <?php echo ($paginaActual == 'index.php') ? 'active' : ''; ?>">
                <i class="fa-solid fa-gauge-high"></i> Dashboard
            </a>

            <a href="temas.php" class="list-group-item list-group-item-action list-group-item-dark <?php echo ($paginaActual == 'temas.php') ? 'active' : ''; ?>">
                <i class="fa-solid fa-book-open"></i> Repasar Tema
            </a>

            <a href="practica.php" class="list-group-item list-group-item-action list-group-item-dark <?php echo ($paginaActual == 'practica.php') ? 'active' : ''; ?>">
                <i class="fa-solid fa-puzzle-piece"></i> Practicar
            </a>

            <a href="examenes.php" class="list-group-item list-group-item-action list-group-item-dark <?php echo ($paginaActual == 'examenes.php') ? 'active' : ''; ?>">
                <i class="fa-solid fa-file-signature"></i> Cuestionarios
            </a>

            <div class="sidebar-header mt-2">Administración</div>

            <a href="gestionar.php" class="list-group-item list-group-item-action list-group-item-dark <?php echo ($paginaActual == 'gestionar.php') ? 'active' : ''; ?>">
                <i class="fa-solid fa-database"></i> Banco de Preguntas
            </a>
            
            <a href="agregar.php" class="list-group-item list-group-item-action list-group-item-dark <?php echo ($paginaActual == 'agregar.php') ? 'active' : ''; ?>">
                <i class="fa-solid fa-plus-circle"></i> Añadir Nueva
            </a>

            <div class="sidebar-header mt-2">Sistema</div>
            
            <a href="changelog.php" class="list-group-item list-group-item-action list-group-item-dark <?php echo ($paginaActual == 'changelog.php') ? 'active' : ''; ?>">
                <i class="fa-solid fa-clock-rotate-left"></i> Changelog
            </a>
        </div>

        <div class="mt-auto p-4 text-center">
            <div class="text-white-50 small border-top border-secondary pt-3 opacity-75" style="font-size: 0.7rem;">
                <p class="mb-1">Creado por: <strong class="text-white">Pol Me</strong></p>
                <p class="mb-0">Actualizado por: <strong class="text-white">carlillos79</strong></p>
            </div>
        </div>

    </div>
    
    <div id="page-content-wrapper" class="bg-light">
        <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm sticky-top">
            <div class="container-fluid">
                <button class="btn text-secondary" id="sidebarToggle"><i class="fa-solid fa-bars fa-lg"></i></button>
            </div>
        </nav>
        
        <div class="container-fluid p-4">
