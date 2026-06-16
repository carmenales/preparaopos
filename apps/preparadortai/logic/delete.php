<?php
require_once "../includes/config.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = intval($_POST['id']);
    $type = $_POST['type'];

    if ($type == 'ptype') {
        // 1. Borrar las respuestas incorrectas asociadas (Tabla incorrectas)
        $sql_inc = "DELETE FROM incorrectas WHERE id_pregunta = ?";
        $stmt_inc = mysqli_prepare($link, $sql_inc);
        mysqli_stmt_bind_param($stmt_inc, "i", $id);
        mysqli_stmt_execute($stmt_inc);
        mysqli_stmt_close($stmt_inc);

        // 2. Borrar la pregunta principal (Tabla ptype)
        $sql = "DELETE FROM ptype WHERE id = ?";
        $stmt = mysqli_prepare($link, $sql);
        mysqli_stmt_bind_param($stmt, "i", $id);
        
        if (mysqli_stmt_execute($stmt)) {
            echo "success";
        } else {
            echo "Error al borrar ptype: " . mysqli_error($link);
        }
        mysqli_stmt_close($stmt);

    } elseif ($type == 'rtype') {
        // Borrar solo de la tabla rtype
        $sql = "DELETE FROM rtype WHERE id = ?";
        $stmt = mysqli_prepare($link, $sql);
        mysqli_stmt_bind_param($stmt, "i", $id);
        
        if (mysqli_stmt_execute($stmt)) {
            echo "success";
        } else {
            echo "Error al borrar rtype: " . mysqli_error($link);
        }
        mysqli_stmt_close($stmt);
    } else {
        echo "Tipo no válido";
    }
} else {
    echo "Método no permitido";
}
?>
