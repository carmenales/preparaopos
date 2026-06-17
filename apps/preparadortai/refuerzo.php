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

$weakAreasSql = "
    SELECT
        categoria,
        bloque,
        tema,
        COUNT(*) AS total_answers,
        COALESCE(SUM(is_correct = 1), 0) AS correct_answers,
        COALESCE(SUM(is_correct = 0), 0) AS wrong_answers,
        CASE
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(is_correct = 1) * 100 / COUNT(*), 2)
        END AS accuracy_percentage
    FROM test_attempts
    GROUP BY categoria, bloque, tema
    HAVING total_answers >= 3
    ORDER BY accuracy_percentage ASC, wrong_answers DESC, total_answers DESC
    LIMIT 10
";

$result = mysqli_query($link, $weakAreasSql);
$weakAreas = [];

if ($result) {
    while ($row = mysqli_fetch_assoc($result)) {
        $weakAreas[] = $row;
    }
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="text-primary fw-bold">
        <i class="fa-solid fa-bullseye"></i> Refuerzo
    </h2>

    <a href="estadisticas.php" class="btn btn-outline-primary">
        <i class="fa-solid fa-chart-line"></i> Ver estadísticas
    </a>
</div>

<div class="card shadow-sm border-0 mb-4">
    <div class="card-header bg-white">
        <h5 class="mb-0 fw-bold">
            <i class="fa-solid fa-triangle-exclamation text-primary"></i> Áreas recomendadas
        </h5>
    </div>

    <div class="card-body">
        <?php if (empty($weakAreas)): ?>
            <p class="text-secondary mb-0">
                Todavía no hay suficientes respuestas registradas para generar un modo de refuerzo.
                Responde algunas preguntas más para que esta sección sea útil.
            </p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Categoría</th>
                            <th class="text-end">Bloque</th>
                            <th class="text-end">Tema</th>
                            <th class="text-end">Total</th>
                            <th class="text-end">Aciertos</th>
                            <th class="text-end">Fallos</th>
                            <th class="text-end">% acierto</th>
                            <th class="text-end">Acción</th>
                        </tr>
                    </thead>

                    <tbody>
                        <?php foreach ($weakAreas as $row): ?>
                            <?php
                                $categoria = $row['categoria'] ?? '';
                                $bloque = $row['bloque'];
                                $tema = $row['tema'];

                                $queryParams = [
                                    'categoria' => $categoria,
                                    'modo' => 'refuerzo'
                                ];

                                if ($bloque !== null && $bloque !== '') {
                                    $queryParams['bloque'] = $bloque;
                                }

                                if ($tema !== null && $tema !== '') {
                                    $queryParams['tema'] = $tema;
                                }

                                $testUrl = 'test.php?' . http_build_query($queryParams);
                            ?>

                            <tr>
                                <td><?php echo safe_text($categoria ?: 'Sin categoría'); ?></td>
                                <td class="text-end"><?php echo safe_text($bloque); ?></td>
                                <td class="text-end"><?php echo safe_text($tema); ?></td>
                                <td class="text-end"><?php echo (int)$row['total_answers']; ?></td>
                                <td class="text-end text-success"><?php echo (int)$row['correct_answers']; ?></td>
                                <td class="text-end text-danger fw-bold"><?php echo (int)$row['wrong_answers']; ?></td>
                                <td class="text-end fw-bold"><?php echo format_percentage($row['accuracy_percentage']); ?></td>
                                <td class="text-end">
                                    <a href="<?php echo safe_text($testUrl); ?>" class="btn btn-outline-primary btn-sm">
                                        <i class="fa-solid fa-play"></i> Practicar
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
