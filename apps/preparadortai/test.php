<?php
include 'includes/header.php';

// Funciones auxiliares
function shuffle_assoc($list) {
    if (!is_array($list)) return $list;
    $keys = array_keys($list);
    shuffle($keys);
    $random = array();
    foreach ($keys as $key) { $random[$key] = $list[$key]; }
    return $random;
}

function cmp($a, $b) {
    return strcmp($a[0], $b[0]);
}

$cat = isset($_GET["categoria"]) ? trim($_GET["categoria"]) : '';
$catSafe = htmlspecialchars($cat, ENT_QUOTES, 'UTF-8');

$examen = str_contains($cat, 'CUESTIONARIO');
$modo = isset($_GET['modo']) ? $_GET['modo'] : '';
$filtroBloque = isset($_GET['bloque']) && $_GET['bloque'] !== '' ? (int)$_GET['bloque'] : null;
$filtroTema = isset($_GET['tema']) && $_GET['tema'] !== '' ? (int)$_GET['tema'] : null;

$testSessionId = bin2hex(random_bytes(16));

// Lógica de BD
$whereClauses = ["categoria = ?"];

if ($filtroBloque !== null) {
    $whereClauses[] = "bloque = ?";
}

if ($filtroTema !== null) {
    $whereClauses[] = "tema = ?";
}

$whereSql = implode(" AND ", $whereClauses);

if ($examen) {
    $sql = "select id, pregunta, respuesta, img_path, justif, categoria, bloque, tema from ptype where $whereSql ORDER BY id";
} else {
    $sql = "select id, pregunta, respuesta, img_path, justif, categoria, bloque, tema from ptype where $whereSql ORDER BY RAND()";
}

$stmt = mysqli_prepare($link, $sql);

if ($filtroBloque !== null && $filtroTema !== null) {
    mysqli_stmt_bind_param($stmt, "sii", $cat, $filtroBloque, $filtroTema);
} elseif ($filtroBloque !== null) {
    mysqli_stmt_bind_param($stmt, "si", $cat, $filtroBloque);
} elseif ($filtroTema !== null) {
    mysqli_stmt_bind_param($stmt, "si", $cat, $filtroTema);
} else {
    mysqli_stmt_bind_param($stmt, "s", $cat);
}

mysqli_stmt_execute($stmt);
mysqli_stmt_bind_result($stmt, $id, $pregunta, $respuesta, $img_path, $justif, $categoriaPregunta, $bloquePregunta, $temaPregunta);

$preguntas = [];

while (mysqli_stmt_fetch($stmt)) {
    array_push($preguntas, array($id, $pregunta, $respuesta, $img_path, $justif, $categoriaPregunta, $bloquePregunta, $temaPregunta));
}

mysqli_stmt_close($stmt);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-clipboard-question"></i> <?php echo $catSafe; ?>
    </h2>

    <span class="badge bg-secondary fs-6 rounded-pill"><?php echo count($preguntas); ?> Preguntas</span>
</div>

<?php if ($modo === 'refuerzo'): ?>
    <div class="alert alert-info shadow-sm border-0">
        Modo refuerzo activo
        <?php if ($filtroBloque !== null): ?>
            · Bloque <?php echo (int)$filtroBloque; ?>
        <?php endif; ?>
        <?php if ($filtroTema !== null): ?>
            · Tema <?php echo (int)$filtroTema; ?>
        <?php endif; ?>
    </div>
<?php endif; ?>

<?php if (empty($preguntas)): ?>
    <div class="alert alert-warning shadow-sm border-0">
        No hay preguntas disponibles con los filtros seleccionados.
    </div>

    <a href="refuerzo.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a refuerzo
    </a>
<?php else: ?>
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <?php
            $qIndex = 1;
            foreach ($preguntas as $p) {
                $pId = $p[0];
                $pTexto = $p[1];
                $pCorrecta = $p[2];
                $pImg = $p[3];
                $pJustif = $p[4];
                $pCategoria = $p[5];
                $pBloque = $p[6];
                $pTema = $p[7];

                // Obtener opciones
                $opciones = [];
                array_push($opciones, array($pCorrecta, $pJustif, true));

                if ($examen) {
                    $sql2 = "select respuesta, justif from incorrectas where id_pregunta = ? ORDER BY respuesta";
                } else {
                    $sql2 = "select respuesta, justif from incorrectas where id_pregunta = ? ORDER BY RAND() limit 3";
                }

                $stmt2 = mysqli_prepare($link, $sql2);
                mysqli_stmt_bind_param($stmt2, "s", $pId);
                mysqli_stmt_execute($stmt2);
                mysqli_stmt_bind_result($stmt2, $opcion_inc, $argum_inc);

                while (mysqli_stmt_fetch($stmt2)) {
                    array_push($opciones, array($opcion_inc, $argum_inc, false));
                }

                mysqli_stmt_close($stmt2);

                if (!$examen) {
                    shuffle($opciones);
                } else {
                    usort($opciones, "cmp");
                }
            ?>

            <div class="card mb-5 shadow-sm border-0">
                <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
                    <h5 class="fw-bold text-dark d-flex">
                        <span class="badge bg-primary me-3 align-self-start"><?php echo $qIndex++; ?></span>
                        <span><?php echo htmlspecialchars($pTexto, ENT_QUOTES, 'UTF-8'); ?></span>
                    </h5>
                </div>

                <div class="card-body p-4">
                    <?php if (!empty($pImg)): ?>
                        <div class="text-center mb-4">
                            <img src="assets/img/<?php echo htmlspecialchars($pImg, ENT_QUOTES, 'UTF-8'); ?>" class="img-fluid rounded border shadow-sm" style="max-height: 300px;">
                        </div>
                    <?php endif; ?>

                    <div class="list-group">
                        <?php foreach ($opciones as $opt):
                            $textoOpt = $opt[0];
                            $justifOpt = $opt[1];
                            $esCorrecta = $opt[2] ? 'true' : 'false';
                        ?>
                            <button type="button"
                                    class="list-group-item list-group-item-action opcion-test p-3 border-bottom"
                                    data-test-session-id="<?php echo htmlspecialchars($testSessionId, ENT_QUOTES, 'UTF-8'); ?>"
                                    data-question-id="<?php echo (int) $pId; ?>"
                                    data-selected-answer="<?php echo htmlspecialchars($textoOpt, ENT_QUOTES, 'UTF-8'); ?>"
                                    data-correct-answer="<?php echo htmlspecialchars($pCorrecta, ENT_QUOTES, 'UTF-8'); ?>"
                                    data-categoria="<?php echo htmlspecialchars($pCategoria ?? '', ENT_QUOTES, 'UTF-8'); ?>"
                                    data-bloque="<?php echo htmlspecialchars((string) ($pBloque ?? ''), ENT_QUOTES, 'UTF-8'); ?>"
                                    data-tema="<?php echo htmlspecialchars((string) ($pTema ?? ''), ENT_QUOTES, 'UTF-8'); ?>"
                                    onclick="verificarRespuesta(this, <?php echo $esCorrecta; ?>)">

                                <div class="d-flex w-100 justify-content-between">
                                    <div class="d-flex align-items-start flex-grow-1 me-2">
                                        <i class="fa-regular fa-circle mt-1 me-3 text-secondary icon-state"></i>
                                        <span class="mb-0 fs-6"><?php echo htmlspecialchars($textoOpt, ENT_QUOTES, 'UTF-8'); ?></span>
                                    </div>

                                    <div class="flex-shrink-0">
                                        <i class="fa-solid fa-check text-success d-none icon-result-ok fs-4"></i>
                                        <i class="fa-solid fa-xmark text-danger d-none icon-result-bad fs-4"></i>
                                    </div>
                                </div>

                                <?php if (!empty($justifOpt) || ($esCorrecta == 'true' && !empty($pJustif))): ?>
                                    <div class="alert alert-warning mt-2 mb-0 py-2 small d-none justificacion text-start">
                                        <i class="fa-solid fa-lightbulb me-1 text-warning"></i>
                                        <?php echo htmlspecialchars(($esCorrecta == 'true' && !empty($pJustif)) ? $pJustif : $justifOpt, ENT_QUOTES, 'UTF-8'); ?>
                                    </div>
                                <?php endif; ?>
                            </button>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>
            <?php } ?>
        </div>
    </div>
<?php endif; ?>

<script>
function verificarRespuesta(elemento, esCorrecta) {
    if (elemento.parentElement.classList.contains('answered')) return;

    let parent = elemento.parentElement;
    parent.classList.add('answered');

    let opciones = parent.children;
    for(let i=0; i<opciones.length; i++) {
        opciones[i].classList.add('processed');
        opciones[i].style.cursor = 'default';
    }

    const iconState = elemento.querySelector('.icon-state');

    if (esCorrecta) {
        elemento.classList.add('correct-answer');
        iconState.classList.replace('fa-circle', 'fa-circle-check');
        iconState.classList.add('fa-solid', 'text-success');
    } else {
        elemento.classList.add('wrong-answer');
        iconState.classList.replace('fa-circle', 'fa-circle-xmark');
        iconState.classList.add('fa-solid', 'text-danger');
    }

    let justif = elemento.querySelector('.justificacion');
    if(justif) justif.classList.remove('d-none');

    const payload = {
        test_session_id: elemento.dataset.testSessionId,
        question_id: parseInt(elemento.dataset.questionId, 10),
        selected_answer: elemento.dataset.selectedAnswer,
        correct_answer: elemento.dataset.correctAnswer,
        is_correct: esCorrecta ? 1 : 0,
        categoria: elemento.dataset.categoria || null,
        bloque: elemento.dataset.bloque !== '' ? parseInt(elemento.dataset.bloque, 10) : null,
        tema: elemento.dataset.tema !== '' ? parseInt(elemento.dataset.tema, 10) : null
    };

    fetch('logic/save_attempt.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(function(response) {
        if (!response.ok) {
            return response.text().then(function(text) {
                throw new Error('HTTP ' + response.status + ': ' + text);
            });
        }
    })
    .catch(function(error) {
        console.error('Could not save test attempt', error);
    });
}
</script>

<?php include 'includes/footer.php'; ?>
