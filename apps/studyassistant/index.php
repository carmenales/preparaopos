<?php
require_once __DIR__ . '/includes/knowledge.php';
require_once __DIR__ . '/../shared/helpers/url.php';

$notes = sa_load_index();
$query = isset($_GET['q']) ? trim($_GET['q']) : '';
$tag = isset($_GET['tag']) ? trim($_GET['tag']) : '';
$process = isset($_GET['process']) ? trim($_GET['process']) : '';
$status = isset($_GET['status']) ? trim($_GET['status']) : '';
$searchMode = isset($_GET['mode']) && $_GET['mode'] === 'semantic' ? 'semantic' : 'standard';

$tags = sa_collect_unique($notes, 'tags');
$processes = sa_collect_unique($notes, 'processes');
$statuses = sa_collect_statuses($notes);
$filteredNotes = sa_filter_notes($notes, $query, $tag, $process, $status);

// Métricas objetivas para el Dashboard
$totalNotes = count($notes);
$totalProcesses = count($processes);
$totalTags = count($tags);

$reviewedCount = 0;
$draftCount = 0;
foreach ($notes as $n) {
    $st = strtolower((string)($n['status'] ?? ''));
    if (in_array($st, ['revisado', 'publicado', 'completo', 'listo'], true)) {
        $reviewedCount++;
    } else {
        $draftCount++;
    }
}

// Resúmenes por proceso para el Process Hub
$processSummaries = [];
foreach ($processes as $procSlug) {
    $procNotes = array_filter($notes, static function ($n) use ($procSlug) {
        return in_array($procSlug, $n['processes'] ?? [], true);
    });
    $procTotal = count($procNotes);
    if ($procTotal === 0) {
        continue;
    }
    $procReviewed = 0;
    $procDraft = 0;
    $procTagCounts = [];
    foreach ($procNotes as $pn) {
        $st = strtolower((string)($pn['status'] ?? ''));
        if (in_array($st, ['revisado', 'publicado', 'completo', 'listo'], true)) {
            $procReviewed++;
        } else {
            $procDraft++;
        }
        foreach ($pn['tags'] ?? [] as $t) {
            $procTagCounts[$t] = ($procTagCounts[$t] ?? 0) + 1;
        }
    }
    arsort($procTagCounts);
    $topTags = array_slice(array_keys($procTagCounts), 0, 3);

    $processSummaries[$procSlug] = [
        'slug' => $procSlug,
        'title' => sa_format_process_title($procSlug),
        'total' => $procTotal,
        'reviewed' => $procReviewed,
        'draft' => $procDraft,
        'tags' => $topTags,
    ];
}

$reviewedCountInProcess = 0;
$draftCountInProcess = 0;
if ($process !== '') {
    foreach ($filteredNotes as $fn) {
        $st = strtolower((string)($fn['status'] ?? ''));
        if (in_array($st, ['revisado', 'publicado', 'completo', 'listo'], true)) {
            $reviewedCountInProcess++;
        } else {
            $draftCountInProcess++;
        }
    }
}

// Filtros activos para generar chips
$activeFilters = [];
if ($query !== '') {
    $params = $_GET;
    unset($params['q']);
    $activeFilters[] = [
        'name' => 'Búsqueda',
        'value' => $query,
        'remove_url' => 'index.php?' . http_build_query($params),
    ];
}
if ($process !== '') {
    $params = $_GET;
    unset($params['process']);
    $activeFilters[] = [
        'name' => 'Proceso',
        'value' => sa_format_process_title($process),
        'remove_url' => 'index.php?' . http_build_query($params),
    ];
}
if ($tag !== '') {
    $params = $_GET;
    unset($params['tag']);
    $activeFilters[] = [
        'name' => 'Etiqueta',
        'value' => $tag,
        'remove_url' => 'index.php?' . http_build_query($params),
    ];
}
if ($status !== '') {
    $params = $_GET;
    unset($params['status']);
    $activeFilters[] = [
        'name' => 'Estado',
        'value' => ucfirst($status),
        'remove_url' => 'index.php?' . http_build_query($params),
    ];
}

$pageTitle = ($process !== '' ? sa_format_process_title($process) . ' · ' : '') . 'Dashboard de Apuntes · Study Assistant';
require __DIR__ . '/includes/header.php';
?>

<?php if ($process !== ''): ?>
    <!-- Cabecera Dedicada al Proceso Seleccionado -->
    <div class="selected-process-hero">
        <a class="back-to-hub-link" href="index.php">← Volver al catálogo general de procesos</a>
        <div class="selected-process-title-row">
            <div>
                <span class="selected-process-badge">Oposición / Convocatoria</span>
                <h1 class="selected-process-title"><?php echo sa_safe_text(sa_format_process_title($process)); ?></h1>
            </div>
            <div class="selected-process-stats">
                <span class="proc-stat-pill"><strong><?php echo count($filteredNotes); ?></strong> temas</span>
                <span class="proc-stat-pill stat-rev"><strong><?php echo $reviewedCountInProcess; ?></strong> revisados</span>
                <?php if ($draftCountInProcess > 0): ?>
                    <span class="proc-stat-pill stat-draft"><strong><?php echo $draftCountInProcess; ?></strong> en borrador</span>
                <?php endif; ?>
            </div>
        </div>
    </div>
<?php else: ?>
    <section class="hero">
        <h1>Apuntes</h1>
        <p>Consulta, filtra y busca en la base de conocimiento.</p>
    </section>

    <!-- Métricas del Dashboard (KPIs Objetivos) -->
    <section class="kpi-grid">
        <a class="kpi-card" href="index.php" title="Ver todos los apuntes">
            <div class="kpi-icon kpi-icon-blue">📚</div>
            <div class="kpi-content">
                <span class="kpi-val"><?php echo $totalNotes; ?></span>
                <span class="kpi-label">Apuntes Totales</span>
            </div>
        </a>

        <a class="kpi-card" href="#procesos-hub" title="Ver oposiciones y procesos indexados">
            <div class="kpi-icon kpi-icon-purple">🏛️</div>
            <div class="kpi-content">
                <span class="kpi-val"><?php echo $totalProcesses; ?></span>
                <span class="kpi-label">Procesos</span>
            </div>
        </a>

        <a class="kpi-card" href="index.php?status=revisado" title="Filtrar apuntes revisados">
            <div class="kpi-icon kpi-icon-green">✅</div>
            <div class="kpi-content">
                <span class="kpi-val"><?php echo $reviewedCount; ?></span>
                <span class="kpi-label">Revisados</span>
            </div>
        </a>

        <a class="kpi-card" href="index.php?status=borrador" title="Filtrar apuntes en borrador">
            <div class="kpi-icon kpi-icon-amber">📝</div>
            <div class="kpi-content">
                <span class="kpi-val"><?php echo $draftCount; ?></span>
                <span class="kpi-label">En Preparación</span>
            </div>
        </a>
    </section>

    <?php if ($query === '' && $tag === '' && $status === ''): ?>
        <!-- Hub de Procesos Selectivos (Directorio de Convocatorias) -->
        <section class="process-hub-section" id="procesos-hub">
            <div class="section-header-row">
                <div>
                    <h2 class="section-title">🏛️ Convocatorias y Procesos Selectivos</h2>
                    <p class="section-subtitle">Accede directamente al temario completo de cada oposición o consulta una selección de temas destacados abajo.</p>
                </div>
            </div>

            <div class="process-hub-grid">
                <?php foreach ($processSummaries as $pSummary): ?>
                    <div class="process-hub-card">
                        <div class="process-hub-card-header">
                            <div class="process-hub-icon">🏛️</div>
                            <div class="process-hub-title-block">
                                <h3 class="process-hub-name">
                                    <a href="index.php?process=<?php echo urlencode($pSummary['slug']); ?>">
                                        <?php echo sa_safe_text($pSummary['title']); ?>
                                    </a>
                                </h3>
                                <span class="process-hub-slug"><?php echo sa_safe_text($pSummary['slug']); ?></span>
                            </div>
                        </div>

                        <div class="process-hub-metrics">
                            <span class="proc-metric" title="Total de temas disponibles">
                                📚 <strong><?php echo $pSummary['total']; ?></strong> <?php echo $pSummary['total'] === 1 ? 'tema' : 'temas'; ?>
                            </span>
                            <span class="proc-metric text-green" title="Temas con estado revisado">
                                ✅ <strong><?php echo $pSummary['reviewed']; ?></strong> revisados
                            </span>
                            <?php if ($pSummary['draft'] > 0): ?>
                                <span class="proc-metric text-amber" title="Temas en preparación">
                                    📝 <strong><?php echo $pSummary['draft']; ?></strong> borradores
                                </span>
                            <?php endif; ?>
                        </div>

                        <?php if (!empty($pSummary['tags'])): ?>
                            <div class="process-hub-tags">
                                <?php foreach ($pSummary['tags'] as $t): ?>
                                    <span class="tag-mini">#<?php echo sa_safe_text($t); ?></span>
                                <?php endforeach; ?>
                            </div>
                        <?php endif; ?>

                        <div class="process-hub-card-footer">
                            <a class="button-process-enter" href="index.php?process=<?php echo urlencode($pSummary['slug']); ?>">
                                Ver apuntes
                            </a>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </section>
    <?php endif; ?>
<?php endif; ?>

<?php if (empty($notes)): ?>
    <div class="alert">
        No hay índice generado todavía. Ejecuta:
        <code>python scripts/build_knowledge_index.py</code>
    </div>
<?php endif; ?>

<!-- Barra de Búsqueda y Filtros Unificada -->
<section class="dashboard-toolbar">
    <div class="toolbar-header">
        <div class="search-mode-tabs">
            <button
                type="button"
                id="tab-mode-standard"
                class="search-mode-tab <?php echo $searchMode === 'standard' ? 'is-active' : ''; ?>"
                onclick="switchSearchMode('standard')"
            >
                🔍 Filtros de Apuntes
            </button>
            <button
                type="button"
                id="tab-mode-semantic"
                class="search-mode-tab <?php echo $searchMode === 'semantic' ? 'is-active' : ''; ?>"
                onclick="switchSearchMode('semantic')"
            >
                🧠 Búsqueda Semántica (IA)
            </button>
        </div>

        <div class="view-controls">
            <span style="font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase;">Vista:</span>
            <button
                type="button"
                id="btn-view-grid"
                class="view-btn is-active"
                data-view="grid"
                onclick="setViewMode('grid')"
                title="Vista de Cuadrícula con tarjetas completas"
            >
                ⊞ Cuadrícula
            </button>
            <button
                type="button"
                id="btn-view-list"
                class="view-btn"
                data-view="list"
                onclick="setViewMode('list')"
                title="Vista de Lista compacta por temas"
            >
                ☰ Lista compacta
            </button>
        </div>
    </div>

    <!-- Panel de Búsqueda y Filtros Estándar -->
    <div id="panel-search-standard" style="<?php echo $searchMode === 'semantic' ? 'display: none;' : ''; ?>">
        <form class="filters" method="get" action="index.php" style="margin-bottom: 0; padding: 0; border: none; box-shadow: none;">
            <div class="field field-wide">
                <label for="q">Buscar por texto o título</label>
                <input id="q" name="q" type="search" value="<?php echo sa_safe_text($query); ?>" placeholder="Ej. tokenización, redes, docker, ENS...">
            </div>

            <div class="field">
                <label for="process">Proceso selectivo</label>
                <select id="process" name="process">
                    <option value="">Todos los procesos</option>
                    <?php foreach ($processes as $item): ?>
                        <option value="<?php echo sa_safe_text($item); ?>" <?php echo sa_selected_attr($process, $item); ?>>
                            <?php echo sa_safe_text(sa_format_process_title($item)); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="field">
                <label for="tag">Etiqueta clave</label>
                <select id="tag" name="tag">
                    <option value="">Todas las etiquetas</option>
                    <?php foreach ($tags as $item): ?>
                        <option value="<?php echo sa_safe_text($item); ?>" <?php echo sa_selected_attr($tag, $item); ?>>
                            <?php echo sa_safe_text($item); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="field">
                <label for="status">Estado</label>
                <select id="status" name="status">
                    <option value="">Todos los estados</option>
                    <?php foreach ($statuses as $item): ?>
                        <option value="<?php echo sa_safe_text($item); ?>" <?php echo sa_selected_attr($status, $item); ?>>
                            <?php echo sa_safe_text(ucfirst($item)); ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="actions">
                <button type="submit">Filtrar</button>
                <a class="button-secondary" href="index.php">Limpiar</a>
            </div>
        </form>
    </div>

    <!-- Panel de Búsqueda Semántica Integrado -->
    <div id="panel-search-semantic" style="<?php echo $searchMode === 'standard' ? 'display: none;' : ''; ?> margin-top: 10px;">
        <p class="meta" style="margin-top: 0; margin-bottom: 12px;">
            Busca por significado y conceptos clave.
        </p>
        <div class="field field-wide" style="display: flex; gap: 10px; align-items: flex-end;">
            <input id="semantic-q" type="search" placeholder="Escribe tu pregunta o duda (ej. diferencia entre autenticación y autorización, cómo funciona TLS)...">
            <button id="semantic-search-btn" type="button" style="white-space: nowrap;">Consultar IA</button>
        </div>
        <div id="semantic-search-status" class="semantic-search-status" hidden></div>
        <ul id="semantic-search-results" class="semantic-results"></ul>
    </div>

    <!-- Barra de Filtros Activos (Chips) -->
    <?php if (!empty($activeFilters)): ?>
        <div class="active-filters">
            <span class="active-filters-label">Filtros aplicados:</span>
            <?php foreach ($activeFilters as $f): ?>
                <span class="filter-chip">
                    <?php echo sa_safe_text($f['name']); ?>: <strong><?php echo sa_safe_text($f['value']); ?></strong>
                    <a class="filter-chip-remove" href="<?php echo sa_safe_text($f['remove_url']); ?>" title="Quitar filtro">×</a>
                </span>
            <?php endforeach; ?>
            <a class="clear-all-link" href="index.php">Limpiar todos</a>
        </div>
    <?php endif; ?>
</section>

<!-- Agrupación por Procesos -->
<?php
$notesByProcess = [];
foreach ($filteredNotes as $note) {
    $processKey = 'Sin proceso';
    if (!empty($note['processes']) && is_array($note['processes'])) {
        $processKey = (string)$note['processes'][0];
    }
    if (!isset($notesByProcess[$processKey])) {
        $notesByProcess[$processKey] = [];
    }
    $notesByProcess[$processKey][] = $note;
}
foreach ($notesByProcess as $pk => &$pNotes) {
    sa_sort_notes_sequentially($pNotes);
}
unset($pNotes);

$isLimitedPreview = ($process === '' && $query === '' && $tag === '' && $status === '');
$previewLimit = 6;
?>

<div id="procesos" class="accordion-controls">
    <div class="summary" style="margin: 0;">
        <?php if ($process !== ''): ?>
            Mostrando todos los <strong><?php echo count($filteredNotes); ?></strong> temas de <strong><?php echo sa_safe_text(sa_format_process_title($process)); ?></strong>.
        <?php elseif ($isLimitedPreview): ?>
            Mostrando temas · <strong><?php echo $totalNotes; ?></strong> temas en <strong><?php echo count($notesByProcess); ?></strong> convocatorias.
        <?php else: ?>
            Mostrando <strong><?php echo count($filteredNotes); ?></strong> apuntes
            <?php if (count($filteredNotes) < $totalNotes): ?>
                (filtrados de <?php echo $totalNotes; ?> totales)
            <?php endif; ?>
            en <strong><?php echo count($notesByProcess); ?></strong> ámbito(s).
        <?php endif; ?>
    </div>

    <?php if (!empty($notesByProcess)): ?>
        <div>
            <button type="button" class="accordion-toggle-all" onclick="toggleAllAccordions(true)">Expandir todos</button>
            <span style="color: #cbd5e1;">·</span>
            <button type="button" class="accordion-toggle-all" onclick="toggleAllAccordions(false)">Colapsar todos</button>
        </div>
    <?php endif; ?>
</div>

<?php if (empty($filteredNotes)): ?>
    <div class="empty-state">
        <div class="empty-state-icon">🔎</div>
        <h3>No se han encontrado apuntes</h3>
        <p>No hay ningún apunte que coincida con los criterios de búsqueda o filtros seleccionados.</p>
        <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
            <a class="button-secondary" href="index.php">Restablecer filtros</a>
            <button type="button" onclick="switchSearchMode('semantic')" style="background: #2457c5; color: white; border: none; border-radius: 10px; padding: 10px 14px; font-weight: 700; cursor: pointer;">
                Probar Búsqueda Semántica
            </button>
        </div>
    </div>
<?php endif; ?>

<!-- Listado de Grupos de Procesos -->
<?php foreach ($notesByProcess as $processKey => $notesInProcess): ?>
    <?php
    $totalInProcess = count($notesInProcess);
    if ($isLimitedPreview && $totalInProcess > $previewLimit) {
        $displayedNotes = array_slice($notesInProcess, 0, $previewLimit);
        $remainingCount = $totalInProcess - $previewLimit;
    } else {
        $displayedNotes = $notesInProcess;
        $remainingCount = 0;
    }
    ?>
    <details open class="process-accordion" id="proc-<?php echo sa_safe_text(preg_replace('/[^a-zA-Z0-9_-]/', '-', $processKey)); ?>">
        <summary class="process-accordion-summary">
            <div class="process-title-wrapper">
                <span class="process-chevron">▶</span>
                <span><?php echo sa_safe_text(sa_format_process_title($processKey)); ?></span>
                <span class="process-badge-count"><?php echo $totalInProcess; ?></span>
                <?php if ($remainingCount > 0): ?>
                    <span class="preview-badge-pill">Mostrando <?php echo count($displayedNotes); ?> de <?php echo $totalInProcess; ?></span>
                <?php endif; ?>
            </div>

            <?php if ($process !== $processKey && $processKey !== 'Sin proceso'): ?>
                <a
                    class="process-header-enter-btn"
                    href="index.php?process=<?php echo urlencode($processKey); ?>"
                    onclick="event.stopPropagation();"
                    title="Abrir temario completo de este ámbito"
                >
                    Ver todos (<?php echo $totalInProcess; ?>) →
                </a>
            <?php endif; ?>
        </summary>

        <div class="process-accordion-body">
            <div class="notes-view-container is-grid-view">
                <!-- Vista Cuadrícula (Cards) -->
                <div class="note-grid">
                    <?php foreach ($displayedNotes as $note): ?>
                        <?php
                        $practiceTopics = sa_normalize_practice_topics($note);
                        $headingsCount = count($note['headings'] ?? []);
                        $readingTime = sa_estimate_reading_time($note);
                        $statusClass = sa_status_badge_class($note['status'] ?? '');
                        $noteUrl = 'note.php?id=' . urlencode($note['id']);
                        if ($processKey !== 'Sin proceso') {
                            $noteUrl .= '&amp;process=' . urlencode($processKey);
                        }
                        ?>
                        <article class="note-card">
                            <div class="note-card-header">
                                <h3>
                                    <a href="<?php echo $noteUrl; ?>">
                                        <?php echo sa_safe_text($note['title']); ?>
                                    </a>
                                </h3>
                                <?php if (!empty($note['status'])): ?>
                                    <span class="badge <?php echo $statusClass; ?>">
                                        <?php echo sa_safe_text(ucfirst($note['status'])); ?>
                                    </span>
                                <?php endif; ?>
                            </div>

                            <?php if (!empty($note['official_topic'])): ?>
                                <p class="meta" style="font-weight: 600; color: #4338ca; margin: 4px 0 6px;">
                                    <?php echo sa_safe_text($note['official_topic']); ?>
                                </p>
                            <?php endif; ?>

                            <div class="note-meta-badges">
                                <span class="meta-item" title="Número de apartados en este apunte">
                                    📑 <?php echo $headingsCount; ?> <?php echo $headingsCount === 1 ? 'apartado' : 'apartados'; ?>
                                </span>
                                <span class="meta-item" title="Tiempo estimado de lectura">
                                    ⏱️ <?php echo $readingTime; ?>
                                </span>
                                <?php if (!empty($note['shared_with'])): ?>
                                    <span class="meta-item" title="Compartido con otros perfiles">
                                        🔗 <?php echo count($note['shared_with']); ?> compartido(s)
                                    </span>
                                <?php endif; ?>
                            </div>

                            <?php if (!empty($note['excerpt'])): ?>
                                <p class="note-card-excerpt"><?php echo sa_safe_text($note['excerpt']); ?></p>
                            <?php endif; ?>

                            <?php if (!empty($note['tags'])): ?>
                                <div class="tags" style="margin-top: auto; margin-bottom: 12px;">
                                    <?php
                                    $visibleTags = array_slice($note['tags'], 0, 4);
                                    $remainingCountTag = count($note['tags']) - 4;
                                    ?>
                                    <?php foreach ($visibleTags as $noteTag): ?>
                                        <a class="tag" href="index.php?tag=<?php echo urlencode($noteTag); ?>">
                                            <?php echo sa_safe_text($noteTag); ?>
                                        </a>
                                    <?php endforeach; ?>
                                    <?php if ($remainingCountTag > 0): ?>
                                        <span class="tag" style="background: #f1f5f9; color: #64748b;" title="Más etiquetas disponibles en el apunte">
                                            +<?php echo $remainingCountTag; ?> más
                                        </span>
                                    <?php endif; ?>
                                </div>
                            <?php endif; ?>

                            <div class="note-card-footer">
                                <a class="card-action-read" href="<?php echo $noteUrl; ?>">
                                    📖 Ver apunte →
                                </a>

                                <?php if (!empty($practiceTopics)): ?>
                                    <?php
                                    $practiceUrl = build_preparadortai_topic_practice_url(
                                        $practiceTopics,
                                        ['source' => 'studyassistant', 'note' => $note['id'] ?? '']
                                    );
                                    ?>
                                    <a
                                        class="card-action-practice"
                                        href="<?php echo htmlspecialchars($practiceUrl); ?>"
                                        target="_blank"
                                        title="Practicar preguntas tipo test de este tema en Preparador TAI"
                                    >
                                        📝 Practicar test
                                    </a>
                                <?php endif; ?>
                            </div>
                        </article>
                    <?php endforeach; ?>
                </div>

                <!-- Vista Lista Compacta -->
                <div class="note-list-view">
                    <?php foreach ($displayedNotes as $note): ?>
                        <?php
                        $practiceTopics = sa_normalize_practice_topics($note);
                        $headingsCount = count($note['headings'] ?? []);
                        $readingTime = sa_estimate_reading_time($note);
                        $statusClass = sa_status_badge_class($note['status'] ?? '');
                        $noteUrl = 'note.php?id=' . urlencode($note['id']);
                        if ($processKey !== 'Sin proceso') {
                            $noteUrl .= '&amp;process=' . urlencode($processKey);
                        }
                        ?>
                        <div class="note-list-row">
                            <div class="note-list-info">
                                <h4 class="note-list-title">
                                    <a href="<?php echo $noteUrl; ?>">
                                        <?php echo sa_safe_text($note['title']); ?>
                                    </a>
                                </h4>
                                <div class="note-list-meta">
                                    <?php if (!empty($note['official_topic'])): ?>
                                        <span style="font-weight: 600; color: #4338ca;">
                                            <?php echo sa_safe_text($note['official_topic']); ?>
                                        </span>
                                        <span>·</span>
                                    <?php endif; ?>
                                    <span>📑 <?php echo $headingsCount; ?> apartados</span>
                                    <span>·</span>
                                    <span>⏱️ <?php echo $readingTime; ?></span>
                                </div>
                            </div>

                            <div class="note-list-actions">
                                <?php if (!empty($note['status'])): ?>
                                    <span class="badge <?php echo $statusClass; ?>">
                                        <?php echo sa_safe_text(ucfirst($note['status'])); ?>
                                    </span>
                                <?php endif; ?>

                                <?php if (!empty($practiceTopics)): ?>
                                    <?php
                                    $practiceUrl = build_preparadortai_topic_practice_url(
                                        $practiceTopics,
                                        ['source' => 'studyassistant', 'note' => $note['id'] ?? '']
                                    );
                                    ?>
                                    <a
                                        class="card-action-practice"
                                        href="<?php echo htmlspecialchars($practiceUrl); ?>"
                                        target="_blank"
                                        title="Practicar preguntas tipo test en Preparador TAI"
                                    >
                                        📝 Test
                                    </a>
                                <?php endif; ?>

                                <a class="button-secondary" style="padding: 6px 12px; font-size: 13px;" href="<?php echo $noteUrl; ?>">
                                    Ver →
                                </a>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <?php if ($remainingCount > 0): ?>
                    <div class="process-preview-footer">
                        <div class="process-preview-footer-text">
                            Mostrando <strong><?php echo count($displayedNotes); ?></strong> de <strong><?php echo $totalInProcess; ?></strong> temas de esta convocatoria.
                        </div>
                        <a class="button-primary process-preview-more-btn" href="index.php?process=<?php echo urlencode($processKey); ?>">
                            Ver temas
                        </a>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </details>
<?php endforeach; ?>

<script src="assets/semantic-search.js"></script>

<script>
function switchSearchMode(mode) {
    var stdPanel = document.getElementById('panel-search-standard');
    var semPanel = document.getElementById('panel-search-semantic');
    var stdTab = document.getElementById('tab-mode-standard');
    var semTab = document.getElementById('tab-mode-semantic');

    if (mode === 'semantic') {
        if (stdPanel) stdPanel.style.display = 'none';
        if (semPanel) semPanel.style.display = 'block';
        if (stdTab) stdTab.classList.remove('is-active');
        if (semTab) semTab.classList.add('is-active');
        var semInput = document.getElementById('semantic-q');
        if (semInput) semInput.focus();
    } else {
        if (stdPanel) stdPanel.style.display = 'block';
        if (semPanel) semPanel.style.display = 'none';
        if (stdTab) stdTab.classList.add('is-active');
        if (semTab) semTab.classList.remove('is-active');
        var stdInput = document.getElementById('q');
        if (stdInput) stdInput.focus();
    }
}

function setViewMode(mode) {
    var containers = document.querySelectorAll('.notes-view-container');
    containers.forEach(function(el) {
        el.classList.toggle('is-list-view', mode === 'list');
        el.classList.toggle('is-grid-view', mode === 'grid');
    });

    var btnGrid = document.getElementById('btn-view-grid');
    var btnList = document.getElementById('btn-view-list');
    if (btnGrid) btnGrid.classList.toggle('is-active', mode === 'grid');
    if (btnList) btnList.classList.toggle('is-active', mode === 'list');

    try {
        localStorage.setItem('studyassistant_view_mode', mode);
    } catch(e) {}
}

function toggleAllAccordions(open) {
    document.querySelectorAll('.process-accordion').forEach(function(acc) {
        acc.open = Boolean(open);
    });
}

// Inicializar preferencia de vista guardada
(function() {
    try {
        var savedMode = localStorage.getItem('studyassistant_view_mode');
        if (savedMode === 'list' || savedMode === 'grid') {
            setViewMode(savedMode);
        }
    } catch(e) {}
})();
</script>

<?php require __DIR__ . '/includes/footer.php'; ?>
