<?php
include 'includes/header.php';

function safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function format_percentage($value) {
    if ($value === null || $value === '') {
        return '-';
    }

    return number_format((float)$value, 2, ',', '.') . '%';
}

function get_status_badge($answeredQuestions, $totalQuestions) {
    if ($answeredQuestions === 0) {
        return '<span class="badge bg-secondary">Sin respuestas</span>';
    }

    if ($totalQuestions > 0 && $answeredQuestions >= $totalQuestions) {
        return '<span class="badge bg-success">Completa</span>';
    }

    return '<span class="badge bg-warning text-dark">Parcial</span>';
}

$questionSetId = isset($_GET['id']) ? (int)$_GET['id'] : 0;

if ($questionSetId <= 0) {
    ?>
    <div class="alert alert-danger shadow-sm border-0">
        Cuestionario no válido.
    </div>

    <a href="progreso_cuestionarios.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a progreso
    </a>
    <?php
    include 'includes/footer.php';
    exit;
}

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
    WHERE id = ?
";

$stmt = mysqli_prepare($link, $questionSetSql);
mysqli_stmt_bind_param($stmt, "i", $questionSetId);
mysqli_stmt_execute($stmt);
$questionSetResult = mysqli_stmt_get_result($stmt);
$questionSet = mysqli_fetch_assoc($questionSetResult);
mysqli_stmt_close($stmt);

if (!$questionSet) {
    ?>
    <div class="alert alert-warning shadow-sm border-0">
        No se ha encontrado el cuestionario.
    </div>

    <a href="progreso_cuestionarios.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver a progreso
    </a>
    <?php
    include 'includes/footer.php';
    exit;
}

$totalQuestionsSql = "
    SELECT COUNT(*) AS total_questions
    FROM ptype
    WHERE categoria = ?
";

$stmt = mysqli_prepare($link, $totalQuestionsSql);
mysqli_stmt_bind_param($stmt, "s", $questionSet['categoria']);
mysqli_stmt_execute($stmt);
$totalQuestionsResult = mysqli_stmt_get_result($stmt);
$totalQuestionsRow = mysqli_fetch_assoc($totalQuestionsResult);
mysqli_stmt_close($stmt);

$totalQuestions = (int)($totalQuestionsRow['total_questions'] ?? 0);

$sessionsSql = "
    SELECT
        test_session_id,
        MIN(created_at) AS started_at,
        MAX(created_at) AS finished_at,
        COUNT(*) AS answered_questions,
        COALESCE(SUM(is_correct = 1), 0) AS correct_answers,
        COALESCE(SUM(is_correct = 0), 0) AS wrong_answers,
        CASE
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(is_correct = 1) * 100 / COUNT(*), 2)
        END AS accuracy_percentage
    FROM test_attempts
    WHERE
        test_session_id IS NOT NULL
        AND categoria = ?
    GROUP BY test_session_id
    ORDER BY started_at DESC, test_session_id DESC
";

$stmt = mysqli_prepare($link, $sessionsSql);
mysqli_stmt_bind_param($stmt, "s", $questionSet['categoria']);
mysqli_stmt_execute($stmt);
$sessionsResult = mysqli_stmt_get_result($stmt);

$sessions = [];

while ($row = mysqli_fetch_assoc($sessionsResult)) {
    $sessions[] = $row;
}

mysqli_stmt_close($stmt);

$totalSessions = count($sessions);
$completeSessions = 0;
$partialSessions = 0;
$bestAccuracy = null;
$lastSessionDate = null;

foreach ($sessions as $session) {
    $answeredQuestions = (int)$session['answered_questions'];

    if ($totalQuestions > 0 && $answeredQuestions >= $totalQuestions) {
        $completeSessions++;
    } else {
        $partialSessions++;
    }

    if ($bestAccuracy === null || (float)$session['accuracy_percentage'] > $bestAccuracy) {
        $bestAccuracy = (float)$session['accuracy_percentage'];
    }

    if ($lastSessionDate === null) {
        $lastSessionDate = $session['started_at'];
    }
}

$testUrl = 'test.php?categoria=' . urlencode($questionSet['categoria']);
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-clock-rotate-left"></i> Sesiones del cuestionario
    </h2>

    <div class="d-flex gap-2">
        <a href="<?php echo safe_text($testUrl); ?>" class="btn btn-primary">
            <i class="fa-solid fa-play"></i> Hacer cuestionario
        </a>

        <a href="progreso_cuestionarios.php" class="btn btn-outline-primary">
            <i class="fa-solid fa-arrow-left"></i> Volver
        </a>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-clipboard-list text-primary"></i> <?php echo safe_text($questionSet['categoria']); ?>
        </h5>
    </div>

    <div class="card-body">
        <div class="row g-3">
            <div class="col-md-3">
                <div class="text-secondary small text-uppercase fw-bold">Organismo</div>
                <div class="fw-semibold"><?php echo safe_text($questionSet['organismo'] ?: '-'); ?></div>
            </div>

            <div class="col-md-3">
                <div class="text-secondary small text-uppercase fw-bold">Proceso selectivo</div>
                <div class="fw-semibold"><?php echo safe_text($questionSet['proceso_selectivo'] ?: '-'); ?></div>
            </div>

            <div class="col-md-2">
                <div class="text-secondary small text-uppercase fw-bold">Año</div>
                <div class="fw-semibold"><?php echo safe_text($questionSet['convocatoria_year'] ?: '-'); ?></div>
            </div>

            <div class="col-md-2">
                <div class="text-secondary small text-uppercase fw-bold">Turno</div>
                <div class="fw-semibold"><?php echo safe_text($questionSet['turno'] ?: '-'); ?></div>
            </div>

            <div class="col-md-2">
                <div class="text-secondary small text-uppercase fw-bold">Tipo</div>
                <div class="fw-semibold"><?php echo safe_text($questionSet['tipo'] ?: '-'); ?></div>
            </div>
        </div>

        <?php if (!empty($questionSet['descripcion'])): ?>
            <hr>
            <p class="mb-0 text-secondary"><?php echo safe_text($questionSet['descripcion']); ?></p>
        <?php endif; ?>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Preguntas</div>
                <div class="display-6 fw-bold text-dark"><?php echo $totalQuestions; ?></div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Sesiones</div>
                <div class="display-6 fw-bold text-primary"><?php echo $totalSessions; ?></div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Completas / Parciales</div>
                <div class="fs-4 fw-bold">
                    <span class="text-success"><?php echo $completeSessions; ?></span>
                    /
                    <span class="text-warning"><?php echo $partialSessions; ?></span>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
                <div class="text-secondary small text-uppercase fw-bold">Mejor resultado</div>
                <div class="display-6 fw-bold text-success"><?php echo format_percentage($bestAccuracy); ?></div>
            </div>
        </div>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-list-check text-primary"></i> Historial de sesiones
        </h5>
    </div>

    <div class="card-body">
        <?php if (empty($sessions)): ?>
            <p class="text-secondary mb-0">Todavía no hay sesiones registradas para este cuestionario.</p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Fecha inicio</th>
                            <th>Fecha fin</th>
                            <th class="text-end">Respondidas</th>
                            <th class="text-end">Aciertos</th>
                            <th class="text-end">Fallos</th>
                            <th class="text-end">% acierto</th>
                            <th class="text-end">Estado</th>
                            <th class="text-end">Acciones</th>
                        </tr>
                    </thead>

                    <tbody>
                        <?php foreach ($sessions as $session): ?>
                            <?php
                                $answeredQuestions = (int)$session['answered_questions'];
                                $detailUrl = 'detalle_sesion.php?session_id=' . urlencode($session['test_session_id']);
                            ?>

                            <tr>
                                <td><?php echo safe_text($session['started_at']); ?></td>
                                <td><?php echo safe_text($session['finished_at']); ?></td>
                                <td class="text-end"><?php echo $answeredQuestions; ?> / <?php echo $totalQuestions; ?></td>
                                <td class="text-end text-success"><?php echo (int)$session['correct_answers']; ?></td>
                                <td class="text-end text-danger"><?php echo (int)$session['wrong_answers']; ?></td>
                                <td class="text-end fw-bold"><?php echo format_percentage($session['accuracy_percentage']); ?></td>
                                <td class="text-end">
                                    <?php echo get_status_badge($answeredQuestions, $totalQuestions); ?>
                                </td>
                                <td class="text-end">
                                    <a href="<?php echo safe_text($detailUrl); ?>" class="btn btn-outline-secondary btn-sm">
                                        <i class="fa-solid fa-eye"></i> Ver detalle
                                    </a>
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
