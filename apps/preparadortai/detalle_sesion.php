<?php
include 'includes/header.php';
require_once __DIR__ . '/../shared/helpers/url.php';

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
    if ($value === null || $value === '') {
        return '-';
    }

    return number_format((float)$value, $decimals, ',', '.');
}

function format_score_scale($value) {
    if ($value === null || $value === '') {
        return '10';
    }

    $floatValue = (float)$value;

    if (abs($floatValue - round($floatValue)) < 0.0001) {
        return (string)(int)round($floatValue);
    }

    return format_decimal($floatValue);
}

function is_official_exam_question_set($questionSet) {
    return ($questionSet['tipo'] ?? '') === 'Examen oficial';
}

function has_official_scoring_rule($questionSet) {
    return is_official_exam_question_set($questionSet)
        && ($questionSet['scoring_rule_code'] ?? '') !== ''
        && ($questionSet['correct_score'] ?? null) !== null
        && ($questionSet['wrong_penalty'] ?? null) !== null;
}

function calculate_official_score_from_rule($correctAnswers, $wrongAnswers, $blankAnswers, $totalQuestions, $questionSet) {
    if ($totalQuestions <= 0 || !has_official_scoring_rule($questionSet)) {
        return null;
    }

    $correctScore = (float)$questionSet['correct_score'];
    $wrongPenalty = (float)$questionSet['wrong_penalty'];
    $blankScore = (float)($questionSet['blank_score'] ?? 0);
    $scoreScale = (float)($questionSet['score_scale'] ?? 10);
    $minScoreZero = (int)($questionSet['min_score_zero'] ?? 1) === 1;

    if ($correctScore <= 0 || $scoreScale <= 0) {
        return null;
    }

    $rawDirectScore = ($correctAnswers * $correctScore)
        - ($wrongAnswers * $wrongPenalty)
        + ($blankAnswers * $blankScore);

    $directScore = $minScoreZero ? max(0, $rawDirectScore) : $rawDirectScore;
    $score = $directScore * $scoreScale / ($totalQuestions * $correctScore);
    $passThreshold = $scoreScale / 2;

    return [
        'raw_direct_score' => $rawDirectScore,
        'direct_score' => round($directScore, 2),
        'score' => round($score, 2),
        'score_scale' => $scoreScale,
        'pass_threshold' => $passThreshold,
        'passed' => round($score, 2) >= $passThreshold,
        'correct_score' => $correctScore,
        'wrong_penalty' => $wrongPenalty,
        'blank_score' => $blankScore,
        'min_score_zero' => $minScoreZero,
    ];
}

function session_topics_array($raw) {
    $raw = trim((string)$raw);

    if ($raw === '') {
        return [];
    }

    return array_values(array_filter(array_map('trim', explode('||', $raw))));
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

$sessionMetadataSql = "
    SELECT
        ts.id,
        ts.mode,
        ts.title,
        ts.correction_mode,
        ts.total_questions,
        GROUP_CONCAT(tst.topic_label ORDER BY tst.position SEPARATOR '||') AS session_topics
    FROM test_sessions ts
    LEFT JOIN test_session_topics tst
        ON tst.test_session_id = ts.id
    WHERE ts.id = ?
    GROUP BY ts.id, ts.mode, ts.title, ts.correction_mode, ts.total_questions
";

$stmt = mysqli_prepare($link, $sessionMetadataSql);
mysqli_stmt_bind_param($stmt, 's', $sessionId);
mysqli_stmt_execute($stmt);
$sessionMetadataResult = mysqli_stmt_get_result($stmt);
$sessionMetadata = mysqli_fetch_assoc($sessionMetadataResult) ?: null;
mysqli_stmt_close($stmt);

$isThematic = ($sessionMetadata['mode'] ?? '') === 'tematico';
$sessionTopics = session_topics_array($sessionMetadata['session_topics'] ?? '');

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
$sessionTitle = $isThematic
    ? (string)($sessionMetadata['title'] ?? 'Práctica temática')
    : $category;
$failedReviewUrl = 'test.php?modo=falladas&session_id=' . urlencode($summary['test_session_id']);

$questionSet = null;
$totalCategoryQuestions = 0;
$blankAnswers = 0;
$officialScore = null;
$hasOfficialScoring = false;

$questionSetSql = "
    SELECT
        qs.id,
        qs.categoria,
        qs.organismo,
        qs.proceso_selectivo,
        qs.convocatoria_year,
        qs.turno,
        qs.tipo,
        qs.descripcion,
        qs.scoring_rule_id,
        sr.code AS scoring_rule_code,
        sr.name AS scoring_rule_name,
        sr.correct_score,
        sr.wrong_penalty,
        sr.blank_score,
        sr.score_scale,
        sr.min_score_zero
    FROM question_sets qs
    LEFT JOIN scoring_rules sr
        ON sr.id = qs.scoring_rule_id
    WHERE qs.categoria = ?
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
$hasOfficialScoring = !$isThematic && $questionSet && has_official_scoring_rule($questionSet);

if ($isThematic) {
    $totalCategoryQuestions = max(
        $totalAnswers,
        (int)($sessionMetadata['total_questions'] ?? $totalAnswers)
    );
    $blankAnswers = max(0, $totalCategoryQuestions - $totalAnswers);
}

if ($hasOfficialScoring && $totalCategoryQuestions > 0) {
    $blankAnswers = max(0, $totalCategoryQuestions - $totalAnswers);
    $officialScore = calculate_official_score_from_rule(
        $correctAnswers,
        $wrongAnswers,
        $blankAnswers,
        $totalCategoryQuestions,
        $questionSet
    );
}

$attemptsSql = "
    SELECT
        ta.id,
        ta.question_id,
        p.pregunta,
        ta.selected_answer,
        COALESCE(ta.correct_answer, p.respuesta) AS correct_answer,
        ta.is_correct,
        ta.categoria,
        ta.bloque,
        ta.tema,
        ta.created_at
    FROM test_attempts ta
    LEFT JOIN ptype p
        ON p.id = ta.question_id
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
    <div>
        <h2 class="text-primary fw-bold mb-1">
            <i class="fa-solid fa-list-check"></i> Detalle de sesión
        </h2>
        <?php if ($isThematic): ?>
            <div class="text-secondary"><?php echo safe_text($sessionTitle); ?></div>
        <?php endif; ?>
    </div>

    <div class="d-flex gap-2">
        <?php if ($wrongAnswers > 0): ?>
            <a href="<?php echo safe_text($failedReviewUrl); ?>" class="btn btn-outline-danger">
                <i class="fa-solid fa-rotate-left"></i> Repasar falladas
            </a>
        <?php endif; ?>

        <?php if ($sessionMetadata['mode'] === 'tematico'): ?>
            <a class="btn btn-outline-secondary" href="<?php echo get_study_url(); ?>">
                <i class="fa-solid fa-book"></i> Volver a Study Assistant
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

<?php if ($isThematic && !empty($sessionTopics)): ?>
    <div class="alert alert-info shadow-sm border-0">
        <strong>Temáticas:</strong>
        <?php foreach ($sessionTopics as $topicLabel): ?>
            <span class="badge rounded-pill bg-info text-dark ms-1"><?php echo safe_text($topicLabel); ?></span>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">
                    <?php echo $isThematic ? 'Sesión' : 'Categoría'; ?>
                </div>
                <div class="fs-5 fw-bold text-dark">
                    <?php echo safe_text($isThematic ? $sessionTitle : ($summary['categoria'] ?: 'Sin categoría')); ?>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">
                    <?php echo ($hasOfficialScoring || $isThematic) ? 'Contestadas / total' : 'Respuestas'; ?>
                </div>
                <div class="display-6 fw-bold text-dark">
                    <?php if ($hasOfficialScoring || $isThematic): ?>
                        <?php echo (int)$totalAnswers; ?> / <?php echo (int)$totalCategoryQuestions; ?>
                    <?php else: ?>
                        <?php echo (int)$summary['total_answers']; ?>
                    <?php endif; ?>
                </div>
                <?php if ($hasOfficialScoring || $isThematic): ?>
                    <div class="text-secondary small">
                        Blancas: <?php echo (int)$blankAnswers; ?>
                    </div>
                <?php endif; ?>
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
                <?php if ($hasOfficialScoring || $isThematic): ?>
                    <div class="text-secondary small">
                        No contestadas: <?php echo (int)$blankAnswers; ?>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">% acierto contestadas</div>
                <div class="display-6 fw-bold text-primary">
                    <?php echo format_percentage($summary['accuracy_percentage']); ?>
                </div>
                <?php if ($hasOfficialScoring && $officialScore !== null): ?>
                    <div class="text-secondary small">
                        Nota oficial: <?php echo format_decimal($officialScore['score']); ?> / <?php echo format_score_scale($officialScore['score_scale']); ?>
                    </div>
                <?php endif; ?>
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
                    <div class="text-secondary small">
                        sobre <?php echo format_score_scale($officialScore['score_scale']); ?>
                    </div>
                </div>

                <div class="col-md-3">
                    <div class="text-secondary small text-uppercase fw-bold">Referencia</div>
                    <?php if ($officialScore['passed']): ?>
                        <span class="badge bg-success fs-6">≥ <?php echo format_decimal($officialScore['pass_threshold']); ?></span>
                    <?php else: ?>
                        <span class="badge bg-danger fs-6">&lt; <?php echo format_decimal($officialScore['pass_threshold']); ?></span>
                    <?php endif; ?>
                    <div class="text-secondary small mt-1">
                        Mitad de la escala configurada
                    </div>
                </div>

                <div class="col-md-3">
                    <div class="text-secondary small text-uppercase fw-bold">Total / blanco</div>
                    <div class="fs-4 fw-bold text-dark">
                        <?php echo (int)$totalCategoryQuestions; ?>
                        /
                        <?php echo (int)$blankAnswers; ?>
                    </div>
                    <div class="text-secondary small">preguntas del examen / no contestadas</div>
                </div>

                <div class="col-md-3">
                    <div class="text-secondary small text-uppercase fw-bold">Puntuación directa</div>
                    <div class="fs-4 fw-bold text-dark">
                        <?php echo format_decimal($officialScore['direct_score']); ?>
                    </div>
                    <div class="text-secondary small">
                        <?php echo (int)$correctAnswers; ?> aciertos,
                        <?php echo (int)$wrongAnswers; ?> fallos,
                        <?php echo (int)$blankAnswers; ?> blancas
                    </div>
                </div>
            </div>

            <hr>

            <div class="small text-secondary">
                <strong>Regla aplicada:</strong>
                <?php echo safe_text($questionSet['scoring_rule_name'] ?: $questionSet['scoring_rule_code']); ?>.
                Correcta +<?php echo format_decimal($officialScore['correct_score'], 4); ?>,
                errónea -<?php echo format_decimal($officialScore['wrong_penalty'], 4); ?>,
                no contestada <?php echo format_decimal($officialScore['blank_score'], 4); ?>.
                <?php if ($officialScore['min_score_zero']): ?>
                    La puntuación directa negativa se recorta a 0.
                <?php endif; ?>
            </div>

            <?php if ($totalAnswers < $totalCategoryQuestions): ?>
                <div class="alert alert-warning mt-3 mb-0">
                    Esta sesión tiene menos respuestas registradas que preguntas del examen.
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
            <p class="mb-1">
                <strong>Tipo:</strong>
                <?php echo safe_text($questionSet['tipo'] ?: '-'); ?>
                <?php if (!empty($questionSet['organismo']) || !empty($questionSet['proceso_selectivo'])): ?>
                    · <?php echo safe_text(trim(($questionSet['organismo'] ?? '') . ' ' . ($questionSet['proceso_selectivo'] ?? ''))); ?>
                <?php endif; ?>
            </p>

            <?php if ($hasOfficialScoring): ?>
                <p class="mb-0">
                    <strong>Regla de puntuación:</strong>
                    <?php echo safe_text($questionSet['scoring_rule_name'] ?: $questionSet['scoring_rule_code']); ?>
                </p>
            <?php endif; ?>
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
                En los exámenes oficiales con regla de puntuación configurada, el detalle muestra también las preguntas no contestadas.
                Las no contestadas cuentan como blanco según la regla asociada al cuestionario.
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
                                        <span class="text-secondary">No contestada</span>
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
