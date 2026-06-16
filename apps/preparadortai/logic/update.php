<?php
require_once "../includes/config.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // Recoger datos comunes
    $id = intval($_POST['id']);
    $type = $_POST['type'];
    $categoria = $_POST['categoria'];
    $bloque = intval($_POST['bloque']);
    $tema = intval($_POST['tema']);
    $pregunta = $_POST['pregunta'];
    $correcta = $_POST['correcta'];

    if ($type == 'ptype') {
        $justif = $_POST['justificacion'];

        // 1. Actualizar tabla principal
        $sql = "UPDATE ptype SET categoria=?, bloque=?, tema=?, pregunta=?, respuesta=?, justif=? WHERE id=?";
        $stmt = mysqli_prepare($link, $sql);
        mysqli_stmt_bind_param($stmt, "siisssi", $categoria, $bloque, $tema, $pregunta, $correcta, $justif, $id);
        
        if (!mysqli_stmt_execute($stmt)) {
            echo "Error SQL Ptype: " . mysqli_error($link);
            exit;
        }
        mysqli_stmt_close($stmt);

        // 2. Gestionar Incorrectas (Borrar viejas -> Insertar nuevas)
        // Borramos las anteriores para esa pregunta
        $delSql = "DELETE FROM incorrectas WHERE id_pregunta = ?";
        $delStmt = mysqli_prepare($link, $delSql);
        mysqli_stmt_bind_param($delStmt, "i", $id);
        mysqli_stmt_execute($delStmt);
        mysqli_stmt_close($delStmt);

        // Insertamos las que vienen del formulario
        if (isset($_POST['field_name'])) {
            $incorrectas = $_POST['field_name']; // Array
            $justifs_inc = $_POST['justif_name']; // Array

            $insSql = "INSERT INTO incorrectas (id_pregunta, respuesta, justif) VALUES (?, ?, ?)";
            $insStmt = mysqli_prepare($link, $insSql);

            for ($i = 0; $i < count($incorrectas); $i++) {
                $txt = trim($incorrectas[$i]);
                $jus = trim($justifs_inc[$i]);
                if (!empty($txt)) {
                    mysqli_stmt_bind_param($insStmt, "iss", $id, $txt, $jus);
                    mysqli_stmt_execute($insStmt);
                }
            }
            mysqli_stmt_close($insStmt);
        }
        echo "success";

    } elseif ($type == 'rtype') {
        // Actualizar tabla rtype (más simple)
        $sql = "UPDATE rtype SET categoria=?, bloque=?, tema=?, pregunta=?, respuesta=? WHERE id=?";
        $stmt = mysqli_prepare($link, $sql);
        mysqli_stmt_bind_param($stmt, "siissi", $categoria, $bloque, $tema, $pregunta, $correcta, $id);
        
        if (mysqli_stmt_execute($stmt)) {
            echo "success";
        } else {
            echo "Error SQL Rtype: " . mysqli_error($link);
        }
        mysqli_stmt_close($stmt);
    }

} else {
    echo "Método no válido.";
}
?>
