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
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-list-check"></i> Detalle de sesión
    </h2>

    <a href="estadisticas.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-arrow-left"></i> Volver
    </a>
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

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-clock text-primary"></i> Información de la sesión
        </h5>
    </div>

    <div class="card-body">
        <p class="mb-1"><strong>Inicio:</strong> <?php echo safe_text($summary['started_at']); ?></p>
        <p class="mb-1"><strong>Fin:</strong> <?php echo safe_text($summary['finished_at']); ?></p>
        <p class="mb-0"><strong>ID sesión:</strong> <code><?php echo safe_text($summary['test_session_id']); ?></code></p>
    </div>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-clipboard-question text-primary"></i> Respuestas de la sesión
        </h5>
    </div>

    <div class="card-body">
        <?php if (empty($attempts)): ?>
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
                        <?php foreach ($attempts as $row): ?>
                            <tr>
                                <td style="max-width: 480px;">
                                    <div class="fw-semibold">
                                        <?php echo safe_text($row['pregunta'] ?: 'Pregunta no encontrada'); ?>
                                    </div>
                                    <div class="text-secondary small">
                                        ID pregunta: <?php echo (int)$row['question_id']; ?>
                                    </div>
                                </td>

                                <td><?php echo safe_text($row['selected_answer']); ?></td>
                                <td><?php echo safe_text($row['correct_answer']); ?></td>

                                <td class="text-center">
                                    <?php if ((int)$row['is_correct'] === 1): ?>
                                        <span class="badge bg-success">Correcta</span>
                                    <?php else: ?>
                                        <span class="badge bg-danger">Fallada</span>
                                    <?php endif; ?>
                                </td>

                                <td class="text-end"><?php echo safe_text($row['bloque']); ?></td>
                                <td class="text-end"><?php echo safe_text($row['tema']); ?></td>
                                <td class="text-end"><?php echo safe_text($row['created_at']); ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include 'includes/footer.php'; ?>
