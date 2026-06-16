<?php
// CORRECCIÓN: Ajustamos la ruta para encontrar config.php desde la carpeta logic
require_once "../includes/config.php";

// Verificamos que se reciban datos para evitar Warnings
if (!isset($_POST['type'])) {
    echo "Error: No se recibieron datos.";
    exit;
}

$type = $_POST['type'];
$pregunta = $_POST["pregunta"];
$respuesta = $_POST["correcta"];
$categoria = $_POST["categoria"];
$bloque = isset($_POST["bloque"]) ? (int)$_POST["bloque"] : 0;
$tema = isset($_POST["tema"]) ? (int)$_POST["tema"] : 0;

if ($type == "rtype") {
    // Lógica para 'Relacionar'
    $sql = "INSERT INTO rtype (pregunta, respuesta, categoria, bloque, tema) VALUES(?,?,?,?,?)";
    $stmt = mysqli_prepare($link, $sql);
    mysqli_stmt_bind_param($stmt, "sssii", $pregunta, $respuesta, $categoria, $bloque, $tema);
    
    if(mysqli_stmt_execute($stmt)){
        echo "Pregunta de relación guardada correctamente.";
    } else {
        echo "Error al guardar: " . mysqli_error($link);
    }
    mysqli_stmt_close($stmt);

} else {
    // Lógica para 'Test' (Ptype)
    $justif = isset($_POST["justificacion"]) ? $_POST["justificacion"] : "";
    
    $sql = "INSERT INTO ptype (pregunta, respuesta, categoria, bloque, tema, justif) VALUES(?,?,?,?,?,?)";
    $stmt = mysqli_prepare($link, $sql);
    mysqli_stmt_bind_param($stmt, "sssiis", $pregunta, $respuesta, $categoria, $bloque, $tema, $justif);
    
    if(mysqli_stmt_execute($stmt)){
        $inserted_id = mysqli_insert_id($link);
        mysqli_stmt_close($stmt);

        // Guardar incorrectas
        if(isset($_POST['incorrectas']) && is_array($_POST['incorrectas'])){
            $incorrectas = $_POST['incorrectas'];
            $justificaciones = isset($_POST['justif']) ? $_POST['justif'] : [];
            
            $sql_inc = "INSERT INTO incorrectas (id_pregunta, respuesta, justif) VALUES(?,?,?)";
            $stmt_inc = mysqli_prepare($link, $sql_inc);

            for ($i = 0; $i < count($incorrectas); $i++) {
                $opcion = trim($incorrectas[$i]);
                $inc_just = isset($justificaciones[$i]) ? $justificaciones[$i] : "";

                if (!empty($opcion)) {
                    mysqli_stmt_bind_param($stmt_inc, "iss", $inserted_id, $opcion, $inc_just);
                    mysqli_stmt_execute($stmt_inc);
                }
            }
            mysqli_stmt_close($stmt_inc);
        }
        echo "Pregunta tipo Test guardada con éxito (ID: $inserted_id)";
    } else {
        echo "Error al guardar pregunta: " . mysqli_error($link);
    }
}
?>
