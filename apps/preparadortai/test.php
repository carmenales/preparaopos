<?php
include 'includes/header.php';

// Funciones auxiliares
function cmp($a, $b) {
    return strcmp($a[0], $b[0]);
}

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

$cat = isset($_GET["categoria"]) ? trim($_GET["categoria"]) : '';
$modo = isset($_GET['modo']) ? $_GET['modo'] : '';
$failedMode = $modo === 'falladas';
$sessionId = isset($_GET['session_id']) ? trim($_GET['session_id']) : '';

$correccion = isset($_GET['correccion']) ? $_GET['correccion'] : '';
$correccionFinal = $correccion === 'final';

$filtroBloque = isset($_GET['bloque']) && $_GET['bloque'] !== '' ? (int)$_GET['bloque'] : null;
$filtroTema = isset($_GET['tema']) && $_GET['tema'] !== '' ? (int)$_GET['tema'] : null;

$testSessionId = bin2hex(random_bytes(16));
$preguntas = [];
$errorMessage = null;

if ($failedMode && !preg_match('/^[a-f0-9]{32}$/', $sessionId)) {
    $errorMessage = 'Sesión de origen no válida para repasar falladas.';
}

if ($errorMessage === null && $failedMode) {
    $sql = "
        SELECT
            p.id,
            p.pregunta,
            p.respuesta,
            p.img_path,
            p.justif,
            p.categoria,
            p.bloque,
            p.tema
        FROM ptype p
        INNER JOIN (
            SELECT
                question_id,
                MIN(created_at) AS first_failed_at
            FROM test_attempts
            WHERE
                test_session_id = ?
                AND is_correct = 0
            GROUP BY question_id
        ) failed_questions
            ON failed_questions.question_id = p.id
        ORDER BY failed_questions.first_failed_at ASC, p.id ASC
    ";

    $stmt = mysqli_prepare($link, $sql);
    mysqli_stmt_bind_param($stmt, "s", $sessionId);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_bind_result($stmt, $id, $pregunta, $respuesta, $img_path, $justif, $categoriaPregunta, $bloquePregunta, $temaPregunta);

    while (mysqli_stmt_fetch($stmt)) {
        $preguntas[] = array($id, $pregunta, $respuesta, $img_path, $justif, $categoriaPregunta, $bloquePregunta, $temaPregunta);
    }

    mysqli_stmt_close($stmt);

    if (!empty($preguntas)) {
        $cat = $preguntas[0][5] ?? '';
    }
} elseif ($errorMessage === null) {
    $whereClauses = ["categoria = ?"];

    if ($filtroBloque !== null) {
        $whereClauses[] = "bloque = ?";
    }

    if ($filtroTema !== null) {
        $whereClauses[] = "tema = ?";
    }

    $whereSql = implode(" AND ", $whereClauses);
    $examen = str_contains($cat, 'CUESTIONARIO');

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

    while (mysqli_stmt_fetch($stmt)) {
        $preguntas[] = array($id, $pregunta, $respuesta, $img_path, $justif, $categoriaPregunta, $bloquePregunta, $temaPregunta);
    }

    mysqli_stmt_close($stmt);
}

$pageTitle = $failedMode ? 'Repaso de preguntas falladas' : $cat;
if ($failedMode && $cat !== '') {
    $pageTitle .= ' · ' . $cat;
}

$queryParams = $_GET;

if ($correccionFinal) {
    unset($queryParams['correccion']);
    $toggleCorrectionUrl = 'test.php?' . http_build_query($queryParams);
    $toggleCorrectionText = 'Corregir al responder';
    $toggleCorrectionIcon = 'fa-bolt';
} else {
    $queryParams['correccion'] = 'final';
    $toggleCorrectionUrl = 'test.php?' . http_build_query($queryParams);
    $toggleCorrectionText = 'Corregir al final';
    $toggleCorrectionIcon = 'fa-list-check';
}

$emptyBackUrl = $failedMode && preg_match('/^[a-f0-9]{32}$/', $sessionId)
    ? 'detalle_sesion.php?session_id=' . urlencode($sessionId)
    : 'refuerzo.php';

$emptyBackText = $failedMode ? 'Volver al detalle de sesión' : 'Volver a refuerzo';
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-clipboard-question"></i> <?php echo safe_text($pageTitle); ?>
    </h2>

    <div class="d-flex gap-2 align-items-center">
        <?php if (!$failedMode || !empty($preguntas)): ?>
            <a href="<?php echo safe_text($toggleCorrectionUrl); ?>" class="btn btn-outline-primary btn-sm">
                <i class="fa-solid <?php echo safe_text($toggleCorrectionIcon); ?>"></i> <?php echo safe_text($toggleCorrectionText); ?>
            </a>
        <?php endif; ?>

        <span class="badge bg-secondary fs-6 rounded-pill"><?php echo count($preguntas); ?> Preguntas</span>
    </div>
</div>

<div id="save-error-alert" class="alert alert-danger shadow-sm border-0 d-none"></div>

<?php if ($errorMessage !== null): ?>
    <div class="alert alert-danger shadow-sm border-0">
        <?php echo safe_text($errorMessage); ?>
    </div>

    <a href="estadisticas.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a estadísticas
    </a>
<?php elseif ($failedMode): ?>
    <div class="alert alert-info shadow-sm border-0">
        Modo repaso de falladas activo. Estás practicando solo las preguntas falladas de la sesión seleccionada.
        Las respuestas de este repaso se guardarán como una sesión nueva.
    </div>
<?php endif; ?>

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

<?php if ($correccionFinal && $errorMessage === null && !empty($preguntas)): ?>
    <div class="alert alert-secondary shadow-sm border-0">
        Corrección al final activa. Marca una respuesta por pregunta y pulsa <strong>Corregir test</strong>.
    </div>
<?php endif; ?>

<?php if ($errorMessage === null && empty($preguntas)): ?>
    <div class="alert alert-warning shadow-sm border-0">
        <?php if ($failedMode): ?>
            Esta sesión no tiene preguntas falladas para repasar.
        <?php else: ?>
            No hay preguntas disponibles con los filtros seleccionados.
        <?php endif; ?>
    </div>

    <a href="<?php echo safe_text($emptyBackUrl); ?>" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> <?php echo safe_text($emptyBackText); ?>
    </a>
<?php elseif ($errorMessage === null): ?>
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

                $esExamenPregunta = str_contains((string)$pCategoria, 'CUESTIONARIO');

                // Obtener opciones
                $opciones = [];
                $opciones[] = array($pCorrecta, $pJustif, true);

                if ($esExamenPregunta) {
                    $sql2 = "select respuesta, justif from incorrectas where id_pregunta = ? ORDER BY respuesta";
                } else {
                    $sql2 = "select respuesta, justif from incorrectas where id_pregunta = ? ORDER BY RAND() limit 3";
                }

                $stmt2 = mysqli_prepare($link, $sql2);
                mysqli_stmt_bind_param($stmt2, "s", $pId);
                mysqli_stmt_execute($stmt2);
                mysqli_stmt_bind_result($stmt2, $opcion_inc, $argum_inc);

                while (mysqli_stmt_fetch($stmt2)) {
                    $opciones[] = array($opcion_inc, $argum_inc, false);
                }

                mysqli_stmt_close($stmt2);

                if (!$esExamenPregunta) {
                    shuffle($opciones);
                } else {
                    usort($opciones, "cmp");
                }
            ?>

            <div class="card mb-5 shadow-sm border-0 question-card" data-question-card="true">
                <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
                    <h5 class="fw-bold text-dark d-flex">
                        <span class="badge bg-primary me-3 align-self-start"><?php echo $qIndex++; ?></span>
                        <span><?php echo safe_text($pTexto); ?></span>
                    </h5>
                </div>

                <div class="card-body p-4">
                    <?php if (!empty($pImg)): ?>
                        <div class="text-center mb-4">
                            <img src="assets/img/<?php echo safe_text($pImg); ?>" class="img-fluid rounded border shadow-sm" style="max-height: 300px;">
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
                                    data-test-session-id="<?php echo safe_text($testSessionId); ?>"
                                    data-question-id="<?php echo (int) $pId; ?>"
                                    data-selected-answer="<?php echo safe_text($textoOpt); ?>"
                                    data-correct-answer="<?php echo safe_text($pCorrecta); ?>"
                                    data-categoria="<?php echo safe_text($pCategoria ?? ''); ?>"
                                    data-bloque="<?php echo safe_text((string) ($pBloque ?? '')); ?>"
                                    data-tema="<?php echo safe_text((string) ($pTema ?? '')); ?>"
                                    data-is-correct="<?php echo $esCorrecta; ?>"
                                    onclick="verificarRespuesta(this, <?php echo $esCorrecta; ?>)">

                                <div class="d-flex w-100 justify-content-between">
                                    <div class="d-flex align-items-start flex-grow-1 me-2">
                                        <i class="fa-regular fa-circle mt-1 me-3 text-secondary icon-state"></i>
                                        <span class="mb-0 fs-6"><?php echo safe_text($textoOpt); ?></span>
                                    </div>

                                    <div class="flex-shrink-0">
                                        <i class="fa-solid fa-check text-success d-none icon-result-ok fs-4"></i>
                                        <i class="fa-solid fa-xmark text-danger d-none icon-result-bad fs-4"></i>
                                    </div>
                                </div>

                                <?php if (!empty($justifOpt) || ($esCorrecta == 'true' && !empty($pJustif))): ?>
                                    <div class="alert alert-warning mt-2 mb-0 py-2 small d-none justificacion text-start">
                                        <i class="fa-solid fa-lightbulb me-1 text-warning"></i>
                                        <?php echo safe_text(($esCorrecta == 'true' && !empty($pJustif)) ? $pJustif : $justifOpt); ?>
                                    </div>
                                <?php endif; ?>
                            </button>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>
            <?php } ?>

            <?php if ($correccionFinal): ?>
                <div class="card mb-5 shadow-sm border-0">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div>
                            <div class="fw-bold">Corrección al final</div>
                            <div class="text-secondary small">Se guardarán las respuestas seleccionadas cuando corrijas el test.</div>
                        </div>

                        <button type="button" class="btn btn-primary" onclick="corregirTestCompleto()">
                            <i class="fa-solid fa-list-check"></i> Corregir test
                        </button>
                    </div>
                </div>

                <div id="resultado-final" class="alert alert-primary shadow-sm border-0 d-none"></div>
            <?php endif; ?>
        </div>
    </div>
<?php endif; ?>

<script>
const correccionFinal = <?php echo $correccionFinal ? 'true' : 'false'; ?>;

function verificarRespuesta(elemento, esCorrecta) {
    if (correccionFinal) {
        seleccionarRespuestaFinal(elemento);
        return;
    }

    corregirRespuestaInmediata(elemento, esCorrecta, true);
}

function seleccionarRespuestaFinal(elemento) {
    if (elemento.parentElement.classList.contains('answered')) return;

    let parent = elemento.parentElement;
    let opciones = parent.children;

    for (let i = 0; i < opciones.length; i++) {
        opciones[i].classList.remove('active');
        opciones[i].classList.remove('selected-answer');

        const iconState = opciones[i].querySelector('.icon-state');

        if (iconState) {
            iconState.className = 'fa-regular fa-circle mt-1 me-3 text-secondary icon-state';
        }
    }

    elemento.classList.add('active');
    elemento.classList.add('selected-answer');

    const iconState = elemento.querySelector('.icon-state');

    if (iconState) {
        iconState.classList.replace('fa-circle', 'fa-circle-dot');
        iconState.classList.add('fa-solid');
    }
}

function corregirTestCompleto() {
    const questionCards = document.querySelectorAll('[data-question-card="true"]');
    let total = questionCards.length;
    let answered = 0;
    let correct = 0;

    questionCards.forEach(function(card) {
        const selected = card.querySelector('.selected-answer');

        if (!selected) {
            card.classList.add('border', 'border-warning');
            return;
        }

        answered++;
        card.classList.remove('border', 'border-warning');

        const isCorrect = selected.dataset.isCorrect === 'true';

        if (isCorrect) {
            correct++;
        }

        corregirRespuestaInmediata(selected, isCorrect, true);
    });

    const resultBox = document.getElementById('resultado-final');

    if (answered < total) {
        resultBox.classList.remove('d-none', 'alert-primary', 'alert-success');
        resultBox.classList.add('alert-warning');
        resultBox.innerHTML = 'Faltan preguntas por responder: ' + answered + ' de ' + total + '.';
        return;
    }

    const wrong = total - correct;
    const percentage = total === 0 ? 0 : Math.round((correct * 10000) / total) / 100;

    resultBox.classList.remove('d-none', 'alert-warning');
    resultBox.classList.add('alert-success');
    resultBox.innerHTML = 'Resultado final: <strong>' + correct + '</strong> aciertos, <strong>' + wrong + '</strong> fallos. Acierto: <strong>' + percentage.toLocaleString('es-ES') + '%</strong>.';
}

function corregirRespuestaInmediata(elemento, esCorrecta, guardarIntento) {
    if (elemento.parentElement.classList.contains('answered')) return;

    let parent = elemento.parentElement;
    parent.classList.add('answered');

    let opciones = parent.children;

    for (let i = 0; i < opciones.length; i++) {
        opciones[i].classList.add('processed');
        opciones[i].style.cursor = 'default';

        if (opciones[i].dataset.isCorrect === 'true') {
            opciones[i].classList.add('correct-answer');

            const correctIcon = opciones[i].querySelector('.icon-state');

            if (correctIcon) {
                correctIcon.className = 'fa-solid fa-circle-check mt-1 me-3 text-success icon-state';
            }
        }
    }

    const iconState = elemento.querySelector('.icon-state');

    if (esCorrecta) {
        elemento.classList.add('correct-answer');

        if (iconState) {
            iconState.className = 'fa-solid fa-circle-check mt-1 me-3 text-success icon-state';
        }
    } else {
        elemento.classList.add('wrong-answer');

        if (iconState) {
            iconState.className = 'fa-solid fa-circle-xmark mt-1 me-3 text-danger icon-state';
        }
    }

    let justif = elemento.querySelector('.justificacion');

    if (justif) justif.classList.remove('d-none');

    if (guardarIntento) {
        guardarRespuesta(elemento, esCorrecta);
    }
}

function guardarRespuesta(elemento, esCorrecta) {
    const questionId = parseInt(elemento.dataset.questionId, 10);

    if (!elemento.dataset.testSessionId || Number.isNaN(questionId)) {
        mostrarErrorGuardado('No se ha podido preparar el guardado de esta respuesta.');
        return;
    }

    const payload = {
        test_session_id: elemento.dataset.testSessionId,
        question_id: questionId,
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
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(function(response) {
        return response.json().then(function(data) {
            if (!response.ok || !data.success) {
                const errorMessage = data.error || 'Error desconocido al guardar la respuesta.';
                const details = data.details ? ' ' + data.details : '';
                throw new Error(errorMessage + details);
            }

            return data;
        });
    })
    .catch(function(error) {
        mostrarErrorGuardado('No se ha guardado una respuesta. ' + error.message);
        console.error('Could not save test attempt', error);
    });
}

function mostrarErrorGuardado(message) {
    const alert = document.getElementById('save-error-alert');

    if (!alert) {
        return;
    }

    alert.textContent = message;
    alert.classList.remove('d-none');
}
</script>

<?php include 'includes/footer.php'; ?>
