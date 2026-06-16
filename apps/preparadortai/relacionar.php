<?php 
// 1. Incluimos el header (que ya carga la config y el diseño)
include 'includes/header.php'; 

// Función auxiliar para mezclar arrays asociativos
function shuffle_assoc($list) {
    if (!is_array($list)) return $list;
    $keys = array_keys($list);
    shuffle($keys);
    $random = array();
    foreach ($keys as $key) {
        $random[$key] = $list[$key];
    }
    return $random;
}

// 2. Lógica de PHP (Recuperamos los datos)
$cat = isset($_GET["categoria"]) ? htmlspecialchars($_GET["categoria"]) : '';
if(empty($cat)){
    echo "<div class='alert alert-danger'>No se ha especificado una categoría.</div>";
    include 'includes/footer.php';
    exit;
}

$sql = "select pregunta, respuesta from rtype where categoria = ?";
$stmt = mysqli_prepare($link, $sql);
mysqli_stmt_bind_param($stmt, "s", $cat);
mysqli_stmt_execute($stmt);
mysqli_stmt_bind_result($stmt, $pregunta, $respuesta);

$array = [];
$respuestas = [];
$arrayIncorrectas = []; // Para saber a qué pregunta pertenecía una respuesta errónea

while (mysqli_stmt_fetch($stmt)) {
  // Key = Pregunta, Value = Respuesta Correcta
  $array[$pregunta] = $respuesta;
  // Key = Respuesta, Value = Pregunta original (para mostrar al fallar)
  $arrayIncorrectas[$respuesta] = $pregunta;
  array_push($respuestas, $respuesta);
}
mysqli_stmt_close($stmt);

// Mezclamos las preguntas
$array = shuffle_assoc($array);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="text-primary fw-bold"><i class="fa-solid fa-arrows-left-right"></i> Práctica de Relacionar</h2>
        <p class="text-muted mb-0">Tema: <strong><?php echo $cat; ?></strong></p>
    </div>
    <a href="index.php" class="btn btn-outline-secondary btn-sm"><i class="fa-solid fa-arrow-left"></i> Volver</a>
</div>

<div class="row justify-content-center">
    <div class="col-lg-10">
    
    <?php if(empty($array)): ?>
        <div class="alert alert-info">No hay preguntas disponibles para esta categoría.</div>
    <?php endif; ?>

    <?php 
    $counter = 1;
    foreach ($array as $preguntaTexto => $respuestaCorrecta) { 
        // Generar opciones (3 incorrectas + 1 correcta)
        $opciones = [];
        $intentos = 0;
        
        // Buscar 3 incorrectas aleatorias
        while (count($opciones) < 3 && $intentos < 50) {
            $rand_key = array_rand($respuestas);
            $posibleRespuesta = $respuestas[$rand_key];
            
            // Que no sea la correcta y que no la hayamos añadido ya
            if ($posibleRespuesta != $respuestaCorrecta && !in_array($posibleRespuesta, $opciones)) {
                $opciones[] = $posibleRespuesta;
            }
            $intentos++;
        }
        
        // Añadir la correcta y barajar
        $opciones[] = $respuestaCorrecta;
        shuffle($opciones);
    ?>

    <div class="card mb-4 shadow-sm border-0">
        <div class="card-body">
            <h5 class="card-title fw-bold text-dark mb-3">
                <span class="badge bg-secondary me-2">#<?php echo $counter++; ?></span>
                <?php echo $preguntaTexto; ?>
            </h5>

            <div class="row g-2">
                <?php foreach ($opciones as $valor): 
                    $esCorrecta = ($valor == $respuestaCorrecta) ? 'true' : 'false';
                    // Si es incorrecta, recuperamos a qué pregunta pertenecía realmente para la explicación
                    $explicacion = ($esCorrecta == 'false' && isset($arrayIncorrectas[$valor])) ? $arrayIncorrectas[$valor] : '';
                ?>
                <div class="col-md-6">
                    <button class="btn btn-outline-dark w-100 text-start p-3 h-100 position-relative btn-relacionar"
                            onclick="verificarRelacion(this, <?php echo $esCorrecta; ?>, '<?php echo addslashes($explicacion); ?>')">
                        <i class="fa-regular fa-circle me-2 icon-state"></i>
                        <?php echo $valor; ?>
                    </button>
                </div>
                <?php endforeach; ?>
            </div>
            
            <div class="feedback-msg mt-2"></div>
        </div>
    </div>

    <?php } ?>
    </div>
</div>

<script>
function verificarRelacion(btn, esCorrecta, explicacionError) {
    // Bloquear el botón para no pulsar dos veces
    if(btn.classList.contains('disabled')) return;

    const icon = btn.querySelector('.icon-state');
    const cardBody = btn.closest('.card-body');
    const feedbackDiv = cardBody.querySelector('.feedback-msg');

    if (esCorrecta) {
        // Estilo Correcto
        btn.classList.remove('btn-outline-dark');
        btn.classList.add('btn-success');
        icon.classList.remove('fa-circle', 'fa-regular');
        icon.classList.add('fa-circle-check', 'fa-solid');
        
        // Deshabilitar todos los botones de esta pregunta
        let siblings = cardBody.querySelectorAll('.btn-relacionar');
        siblings.forEach(b => b.classList.add('disabled'));
        
    } else {
        // Estilo Incorrecto
        btn.classList.remove('btn-outline-dark');
        btn.classList.add('btn-danger');
        icon.classList.remove('fa-circle', 'fa-regular');
        icon.classList.add('fa-circle-xmark', 'fa-solid');
        btn.classList.add('disabled'); // Deshabilitar solo este botón erróneo

        // Mostrar explicación
        if(explicacionError) {
            feedbackDiv.innerHTML = `
                <div class="alert alert-warning animate__animated animate__fadeIn mt-2 py-2 small">
                    <i class="fa-solid fa-triangle-exclamation me-1"></i> 
                    Incorrecto. "<strong>${btn.innerText.trim()}</strong>" corresponde a: <br>
                    <em>${explicacionError}</em>
                </div>
            `;
        }
    }
}
</script>

<?php include 'includes/footer.php'; ?>
