<?php
include 'includes/header.php';

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function format_percentage($value) {
    if ($value === null || $value === '') {
        return '0,00%';
    }

    return number_format((float)$value, 2, ',', '.') . '%';
}

function format_decimal($value, $decimals = 2) {
    return number_format((float)$value, $decimals, ',', '.');
}

function is_ayto_madrid_aux_tic_category($category) {
    return strpos((string)$category, 'AYTO MADRID AUX TIC') === 0;
}

function calculate_official_score($correctAnswers, $wrongAnswers, $totalQuestions) {
    if ($totalQuestions <= 0) {
        return null;
    }

    $penalty = $wrongAnswers / 3;
    $netScore = $correctAnswers - $penalty;
    $score = max(0, $netScore) * 10 / $totalQuestions;

    return [
        'penalty' => $penalty,
        'net_score' => $netScore,
        'score' => round($score, 2),
        'passed' => round($score, 2) >= 5,
    ];
}

$sessionId = isset($_GET['session_id']) ? trim($_GET['session_id']) : '';

if (!preg_match('/^[a-f0-9]{32}$/', $sessionId)) {
    ?>
    <div class="alert alert-danger shadow-sm border-0">
        Sesión no válida.
    </div>

    <a href="estadisticas.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a estadísticas
    </a>
    <?php
    include 'includes/footer.php';
    exit;
}

$summarySql = "
    SELECT
        test_session_id,
        MIN(created_at) AS started_at,
        MAX(created_at) AS finished_at,
        MAX(categoria) AS categoria,
        COUNT(*) AS total_answers,
        COALESCE(SUM(is_correct = 1), 0) AS correct_answers,
        COALESCE(SUM(is_correct = 0), 0) AS wrong_answers,
        CASE
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(is_correct = 1) * 100 / COUNT(*), 2)
        END AS accuracy_percentage
    FROM test_attempts
    WHERE test_session_id = ?
    GROUP BY test_session_id
";

$stmt = mysqli_prepare($link, $summarySql);
mysqli_stmt_bind_param($stmt, "s", $sessionId);
mysqli_stmt_execute($stmt);
$summaryResult = mysqli_stmt_get_result($stmt);
$summary = mysqli_fetch_assoc($summaryResult);
mysqli_stmt_close($stmt);

if (!$summary) {
    ?>
    <div class="alert alert-warning shadow-sm border-0">
        No se han encontrado datos para esta sesión.
    </div>

    <a href="estadisticas.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a estadísticas
    </a>
    <?php
    include 'includes/footer.php';
    exit;
}

$wrongAnswers = (int)$summary['wrong_answers'];
$correctAnswers = (int)$summary['correct_answers'];
$totalAnswers = (int)$summary['total_answers'];
$category = (string)($summary['categoria'] ?? '');
$failedReviewUrl = 'test.php?modo=falladas&session_id=' . urlencode($summary['test_session_id']);

$questionSet = null;
$totalCategoryQuestions = null;
$blankAnswers = null;
$officialScore = null;
$hasOfficialScoring = false;

$questionSetSql = "
    SELECT
        id,
        categoria,
        organismo,
        proceso_selectivo,
        convocatoria_year,
        turno,
        tipo,
        descripcion
    FROM question_sets
    WHERE categoria = ?
    LIMIT 1
";

$stmt = mysqli_prepare($link, $questionSetSql);
mysqli_stmt_bind_param($stmt, "s", $category);
mysqli_stmt_execute($stmt);
$questionSetResult = mysqli_stmt_get_result($stmt);
$questionSet = mysqli_fetch_assoc($questionSetResult);
mysqli_stmt_close($stmt);

$totalQuestionsSql = "
    SELECT COUNT(*) AS total_questions
    FROM ptype
    WHERE categoria = ?
";

$stmt = mysqli_prepare($link, $totalQuestionsSql);
mysqli_stmt_bind_param($stmt, "s", $category);
mysqli_stmt_execute($stmt);
$totalQuestionsResult = mysqli_stmt_get_result($stmt);
$totalQuestionsRow = mysqli_fetch_assoc($totalQuestionsResult);
mysqli_stmt_close($stmt);

$totalCategoryQuestions = (int)($totalQuestionsRow['total_questions'] ?? 0);

if (is_ayto_madrid_aux_tic_category($category) && $totalCategoryQuestions > 0) {
    $hasOfficialScoring = true;
    $blankAnswers = max(0, $totalCategoryQuestions - $totalAnswers);
    $officialScore = calculate_official_score($correctAnswers, $wrongAnswers, $totalCategoryQuestions);
}

$attemptsSql = "
    SELECT
        ta.id,
        ta.question_id,
        p.pregunta,
        ta.selected_answer,
        ta.correct_answer,
        ta.is_correct,
        ta.categoria,
        ta.bloque,
        ta.tema,
        ta.created_at
    FROM test_attempts ta
    LEFT JOIN ptype p ON p.id = ta.question_id
    WHERE ta.test_session_id = ?
    ORDER BY ta.created_at ASC, ta.id ASC
";

$stmt = mysqli_prepare($link, $attemptsSql);
mysqli_stmt_bind_param($stmt, "s", $sessionId);
mysqli_stmt_execute($stmt);
$attemptsResult = mysqli_stmt_get_result($stmt);

$attempts = [];

while ($row = mysqli_fetch_assoc($attemptsResult)) {
    $attempts[] = $row;
}

mysqli_stmt_close($stmt);

$displayAttempts = $attempts;

if ($hasOfficialScoring) {
    $attemptsByQuestionId = [];

    foreach ($attempts as $attempt) {
        $attemptsByQuestionId[(int)$attempt['question_id']] = $attempt;
    }

    $questionsSql = "
        SELECT
            id,
            pregunta,
            respuesta,
            categoria,
            bloque,
            tema
        FROM ptype
        WHERE categoria = ?
        ORDER BY id ASC
    ";

    $stmt = mysqli_prepare($link, $questionsSql);
    mysqli_stmt_bind_param($stmt, "s", $category);
    mysqli_stmt_execute($stmt);
    $questionsResult = mysqli_stmt_get_result($stmt);

    $displayAttempts = [];

    while ($question = mysqli_fetch_assoc($questionsResult)) {
        $questionId = (int)$question['id'];

        if (isset($attemptsByQuestionId[$questionId])) {
            $displayAttempts[] = $attemptsByQuestionId[$questionId];
        } else {
            $displayAttempts[] = [
                'id' => null,
                'question_id' => $questionId,
                'pregunta' => $question['pregunta'],
                'selected_answer' => null,
                'correct_answer' => $question['respuesta'],
                'is_correct' => null,
                'categoria' => $question['categoria'],
                'bloque' => $question['bloque'],
                'tema' => $question['tema'],
                'created_at' => null,
            ];
        }
    }

    mysqli_stmt_close($stmt);
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-list-check"></i> Detalle de sesión
    </h2>

    <div class="d-flex gap-2">
        <?php if ($wrongAnswers > 0): ?>
            <a href="<?php echo safe_text($failedReviewUrl); ?>" class="btn btn-outline-danger">
                <i class="fa-solid fa-rotate-left"></i> Repasar falladas
            </a>
        <?php endif; ?>

        <a href="estadisticas.php" class="btn btn-outline-primary">
            <i class="fa-solid fa-arrow-left"></i> Volver
        </a>

        <form method="post"
            action="logic/delete_test_session.php"
            onsubmit="return confirm('¿Borrar esta sesión de test? Se eliminarán sus respuestas registradas, pero no se borrarán preguntas del banco.');">
            <input type="hidden" name="test_session_id" value="<?php echo safe_text($summary['test_session_id']); ?>">
            <button type="submit" class="btn btn-outline-danger">
                <i class="fa-solid fa-trash"></i> Borrar sesión
            </button>
        </form>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Categoría</div>
                <div class="fs-5 fw-bold text-dark">
                    <?php echo safe_text($summary['categoria'] ?: 'Sin categoría'); ?>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Respuestas</div>
                <div class="display-6 fw-bold text-dark">
                    <?php echo (int)$summary['total_answers']; ?>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Aciertos / Fallos</div>
                <div class="fs-4 fw-bold">
                    <span class="text-success"><?php echo (int)$summary['correct_answers']; ?></span>
                    /
                    <span class="text-danger"><?php echo (int)$summary['wrong_answers']; ?></span>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">% acierto</div>
                <div class="display-6 fw-bold text-primary">
                    <?php echo format_percentage($summary['accuracy_percentage']); ?>
                </div>
            </div>
        </div>
    </div>
</div>

<?php if ($hasOfficialScoring && $officialScore !== null): ?>
    <div class="card shadow-sm border-0 mb-4">
        <div class="card-header bg-white">
            <h5 class="mb-0 fw-bold">
                <i class="fa-solid fa-scale-balanced text-primary"></i> Puntuación oficial estimada
            </h5>
        </div>

        <div class="card-body">
            <div class="row g-4">
                <div class="col-md-3">
                    <div class="text-secondary small text-uppercase fw-bold">Nota</div>
                    <div class="display-6 fw-bold <?php echo $officialScore['passed'] ? 'text-success' : 'text-danger'; ?>">
                        <?php echo format_decimal($officialScore['score']); ?>
                    </div>
                    <div class="text-secondary small">sobre 10</div>
                </div>

                <div class="col-md-3">
                    <div class="text-secondary small text-uppercase fw-bold">Mínimo de la parte</div>
                    <?php if ($officialScore['passed']): ?>
                        <span class="badge bg-success fs-6">Superado</span>
                    <?php else: ?>
                        <span class="badge bg-danger fs-6">No superado</span>
                    <?php endif; ?>
                    <div class="text-secondary small mt-1">Mínimo: 5,00</div>
                </div>

                <div class="col-md-3">
                    <div class="text-secondary small text-uppercase fw-bold">Válidas / blanco</div>
                    <div class="fs-4 fw-bold text-dark">
                        <?php echo (int)$totalCategoryQuestions; ?>
                        /
                        <?php echo (int)$blankAnswers; ?>
                    </div>
                    <div class="text-secondary small">preguntas válidas / no contestadas</div>
                </div>

                <div class="col-md-3">
                    <div class="text-secondary small text-uppercase fw-bold">Puntuación neta</div>
                    <div class="fs-4 fw-bold text-dark">
                        <?php echo format_decimal($officialScore['net_score']); ?>
                    </div>
                    <div class="text-secondary small">
                        <?php echo (int)$correctAnswers; ?> - <?php echo (int)$wrongAnswers; ?>/3
                    </div>
                </div>
            </div>

            <hr>

            <div class="small text-secondary">
                Regla aplicada para Ayuntamiento de Madrid Auxiliar TIC:
                correcta +1, errónea -1/3, no contestada 0.
                La nota se calcula sobre las preguntas válidas de esta categoría y se redondea a dos decimales.
            </div>

            <?php if ($totalAnswers < $totalCategoryQuestions): ?>
                <div class="alert alert-warning mt-3 mb-0">
                    Esta sesión tiene menos respuestas registradas que preguntas válidas en la categoría.
                    Se han considerado <strong><?php echo (int)$blankAnswers; ?></strong> preguntas como no contestadas.
                </div>
            <?php endif; ?>
        </div>
    </div>
<?php endif; ?>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-clock text-primary"></i> Información de la sesión
        </h5>
    </div>

    <div class="card-body">
        <p class="mb-1"><strong>Inicio:</strong> <?php echo safe_text($summary['started_at']); ?></p>
        <p class="mb-1"><strong>Fin:</strong> <?php echo safe_text($summary['finished_at']); ?></p>
        <p class="mb-1"><strong>ID sesión:</strong> <code><?php echo safe_text($summary['test_session_id']); ?></code></p>

        <?php if ($questionSet): ?>
            <p class="mb-0">
                <strong>Tipo:</strong>
                <?php echo safe_text($questionSet['tipo'] ?: '-'); ?>
                <?php if (!empty($questionSet['organismo']) || !empty($questionSet['proceso_selectivo'])): ?>
                    · <?php echo safe_text(trim(($questionSet['organismo'] ?? '') . ' ' . ($questionSet['proceso_selectivo'] ?? ''))); ?>
                <?php endif; ?>
            </p>
        <?php endif; ?>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-clipboard-question text-primary"></i> Respuestas de la sesión
        </h5>
    </div>

    <div class="card-body">
        <?php if ($hasOfficialScoring): ?>
            <div class="alert alert-light border small">
                En los exámenes oficiales, el detalle muestra también las preguntas no contestadas para que puedas ver la respuesta correcta.
                Las no contestadas cuentan como blanco y no penalizan.
            </div>
        <?php endif; ?>

        <?php if (empty($displayAttempts)): ?>
            <p class="text-secondary mb-0">No hay respuestas registradas para esta sesión.</p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Pregunta</th>
                            <th>Respuesta marcada</th>
                            <th>Respuesta correcta</th>
                            <th class="text-center">Resultado</th>
                            <th class="text-end">Bloque</th>
                            <th class="text-end">Tema</th>
                            <th class="text-end">Fecha</th>
                        </tr>
                    </thead>

                    <tbody>
                        <?php foreach ($displayAttempts as $row): ?>
                            <tr>
                                <td style="max-width: 480px;">
                                    <div class="fw-semibold">
                                        <?php echo safe_text($row['pregunta'] ?: 'Pregunta no encontrada'); ?>
                                    </div>
                                    <div class="text-secondary small">
                                        ID pregunta: <?php echo (int)$row['question_id']; ?>
                                    </div>
                                </td>

                                <td>
                                    <?php if ($row['selected_answer'] === null || $row['selected_answer'] === ''): ?>
                                        <span class="text-secondary">—</span>
                                    <?php else: ?>
                                        <?php echo safe_text($row['selected_answer']); ?>
                                    <?php endif; ?>
                                </td>
                                <td><?php echo safe_text($row['correct_answer']); ?></td>

                                <td class="text-center">
                                    <?php if ($row['is_correct'] === null): ?>
                                        <span class="badge bg-secondary">No contestada</span>
                                    <?php elseif ((int)$row['is_correct'] === 1): ?>
                                        <span class="badge bg-success">Correcta</span>
                                    <?php else: ?>
                                        <span class="badge bg-danger">Fallada</span>
                                    <?php endif; ?>
                                </td>

                                <td class="text-end"><?php echo safe_text($row['bloque']); ?></td>
                                <td class="text-end"><?php echo safe_text($row['tema']); ?></td>
                                <td class="text-end">
                                    <?php echo $row['created_at'] === null ? '<span class="text-secondary">—</span>' : safe_text($row['created_at']); ?>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
