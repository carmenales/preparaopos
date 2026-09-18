<?php
require_once __DIR__ . '/includes/knowledge.php';
require_once __DIR__ . '/includes/markdown.php';
require_once __DIR__ . '/../shared/helpers/url.php';

// Manejo de endpoints AJAX proxy para comunicación con el microservicio
$action = $_GET['action'] ?? null;

if ($action !== null) {
    header('Content-Type: application/json; charset=utf-8');
    $serviceUrl = sa_knowledge_service_url();

    // 1. Acción: Extracción de PDF
    if ($action === 'extract') {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            echo json_encode(['error' => 'Método no permitido'], JSON_UNESCAPED_UNICODE);
            exit;
        }

        if (empty($_FILES['pdf_file']) || $_FILES['pdf_file']['error'] !== UPLOAD_ERR_OK) {
            echo json_encode(['error' => 'No se ha subido ningún archivo PDF válido'], JSON_UNESCAPED_UNICODE);
            exit;
        }

        $tmpFile = $_FILES['pdf_file']['tmp_name'];
        $origName = $_FILES['pdf_file']['name'];
        $normalize = isset($_POST['normalize']) ? (string)$_POST['normalize'] : 'true';

        $cfile = new CURLFile($tmpFile, 'application/pdf', $origName);
        $postData = [
            'file' => $cfile,
            'normalize' => $normalize,
        ];

        $ch = curl_init($serviceUrl . '/ingest/extract-pdf');
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $postData,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 180,
        ]);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        if ($curlError) {
            echo json_encode(['error' => 'Error de conexión con el servicio de conocimiento: ' . $curlError], JSON_UNESCAPED_UNICODE);
            exit;
        }

        if ($httpCode >= 400) {
            $errData = json_decode($response, true);
            $msg = $errData['detail'] ?? "Error {$httpCode} al procesar el PDF.";
            echo json_encode(['error' => $msg], JSON_UNESCAPED_UNICODE);
            exit;
        }

        echo $response;
        exit;
    }

    // 2. Acción: Previsualización de Markdown usando el renderizador de StudyAssistant
    if ($action === 'preview') {
        $raw = file_get_contents('php://input');
        $data = json_decode($raw, true) ?: [];
        $markdown = $data['markdown'] ?? '';
        $html = sa_render_markdown($markdown);
        echo json_encode(['html' => $html], JSON_UNESCAPED_UNICODE);
        exit;
    }

    // 3. Acción: Refinado asistido por LLM (Ollama)
    if ($action === 'refine') {
        $raw = file_get_contents('php://input');
        $ch = curl_init($serviceUrl . '/ingest/refine');
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $raw,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 300,
        ]);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        if ($curlError) {
            echo json_encode(['error' => 'Error al conectar con el servicio LLM: ' . $curlError], JSON_UNESCAPED_UNICODE);
            exit;
        }

        if ($httpCode >= 400) {
            $errData = json_decode($response, true);
            $msg = $errData['detail'] ?? "Error {$httpCode} en refinado LLM.";
            echo json_encode(['error' => $msg], JSON_UNESCAPED_UNICODE);
            exit;
        }

        echo $response;
        exit;
    }

    // 4. Acción: Publicación definitiva en la Base de Conocimiento
    if ($action === 'publish') {
        $raw = file_get_contents('php://input');
        $ch = curl_init($serviceUrl . '/ingest/publish');
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $raw,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 60,
        ]);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        if ($curlError) {
            echo json_encode(['error' => 'Error al conectar para publicar: ' . $curlError], JSON_UNESCAPED_UNICODE);
            exit;
        }

        if ($httpCode >= 400) {
            $errData = json_decode($response, true);
            $msg = $errData['detail'] ?? "Error {$httpCode} al publicar la nota.";
            echo json_encode(['error' => $msg], JSON_UNESCAPED_UNICODE);
            exit;
        }

        echo $response;
        exit;
    }

    echo json_encode(['error' => 'Acción no reconocida'], JSON_UNESCAPED_UNICODE);
    exit;
}

// Carga de procesos registrados para el selector
$processesRegistry = sa_load_processes_registry();
$notes = sa_load_index();
$uniqueProcesses = sa_collect_unique($notes, 'processes');

// Unir los procesos del registro con los presentes en las notas
$availableProcesses = [];
foreach ($uniqueProcesses as $pSlug) {
    $availableProcesses[$pSlug] = [
        'id' => $pSlug,
        'title' => $processesRegistry[$pSlug]['title'] ?? sa_format_process_title($pSlug),
    ];
}
foreach ($processesRegistry as $pSlug => $pData) {
    if (!isset($availableProcesses[$pSlug])) {
        $availableProcesses[$pSlug] = [
            'id' => $pSlug,
            'title' => $pData['title'] ?? sa_format_process_title($pSlug),
        ];
    }
}
uasort($availableProcesses, static function ($a, $b) {
    return strnatcasecmp($a['title'], $b['title']);
});

$pageTitle = 'Añadir Apuntes — Study Assistant';
$currentPage = 'ingest';
require_once __DIR__ . '/includes/header.php';
?>

<div class="ingest-container">
    <!-- Encabezado de la herramienta -->
    <header class="ingest-header">
        <div class="ingest-header-titles">
            <span class="ingest-badge">Fuente de Conocimiento</span>
            <h1>Añadir Apuntes</h1>
            <p class="ingest-subtitle">Extrae temarios y apuntes desde PDFs, límpialos con heurísticas inteligentes y publícalos directamente en la base de estudio.</p>
        </div>
    </header>

    <!-- Barra de progreso / Stepper -->
    <div class="ingest-stepper" role="navigation" aria-label="Pasos de ingestión">
        <div class="step-item active" id="stepperStep1">
            <span class="step-number">1</span>
            <span class="step-label">Cargar Documento</span>
        </div>
        <div class="step-arrow">›</div>
        <div class="step-item" id="stepperStep2">
            <span class="step-number">2</span>
            <span class="step-label">Extracción & Análisis</span>
        </div>
        <div class="step-arrow">›</div>
        <div class="step-item" id="stepperStep3">
            <span class="step-number">3</span>
            <span class="step-label">Revisión & Edición</span>
        </div>
        <div class="step-arrow">›</div>
        <div class="step-item" id="stepperStep4">
            <span class="step-number">4</span>
            <span class="step-label">Publicado</span>
        </div>
    </div>

    <!-- PASO 1: Formulario de Subida y Configuración -->
    <section class="ingest-card" id="step1Card">
        <form id="ingestForm" onsubmit="handleExtract(event)">
            <div class="drop-zone" id="dropZone">
                <input type="file" id="pdfFileInput" name="pdf_file" accept=".pdf" class="drop-zone-input" required>
                <div class="drop-zone-content">
                    <div class="drop-zone-icon">📄</div>
                    <h3>Arrastra aquí tu archivo PDF o <span class="browse-link">selecciónalo</span></h3>
                    <p class="drop-zone-hint">Compatible con temarios de academia, convocatorias oficiales y documentos BOE.</p>
                    <div id="fileSelectedBadge" class="file-selected-badge" style="display: none;">
                        <span class="file-name" id="fileNameDisplay">documento.pdf</span>
                        <span class="file-size" id="fileSizeDisplay">0 MB</span>
                    </div>
                </div>
            </div>

            <div class="ingest-grid">
                <div class="form-group">
                    <label for="processSelect">Proceso Selectivo Asignado <span class="required">*</span></label>
                    <select id="processSelect" name="process_slug" required onchange="handleProcessChange(this)">
                        <option value="">-- Seleccionar proceso selectivo --</option>
                        <?php foreach ($availableProcesses as $p): ?>
                            <option value="<?php echo sa_safe_text($p['id']); ?>">
                                <?php echo sa_safe_text($p['title']); ?> (<?php echo sa_safe_text($p['id']); ?>)
                            </option>
                        <?php endforeach; ?>
                        <option value="__new__">+ Crear nuevo proceso selectivo...</option>
                    </select>
                </div>

                <div class="form-group" id="customProcessGroup" style="display: none;">
                    <label for="customProcessInput">Identificador del Nuevo Proceso (slug) <span class="required">*</span></label>
                    <input type="text" id="customProcessInput" placeholder="ej. age/a1-sti o justicia/gestion">
                    <small class="form-hint">Usa minúsculas y guiones separados por barras (ej. organismo/cuerpo).</small>
                </div>

                <div class="form-group">
                    <label for="sourceInput">Origen o Fuente de los Apuntes</label>
                    <input type="text" id="sourceInput" name="source" value="cetic" placeholder="ej. cetic, academia, boe, ia">
                </div>
            </div>

            <div class="ingest-options">
                <label class="checkbox-label">
                    <input type="checkbox" id="optNormalize" name="normalize" value="true" checked>
                    <span><strong>Normalización avanzada</strong> (limpiar cabeceras/pies repetidos, reconstruir párrafos y tablas rotas)</span>
                </label>
            </div>

            <div class="ingest-actions">
                <button type="submit" id="btnExtract" class="btn btn-primary btn-large">
                    <span>⚡ Procesar y Analizar Documento</span>
                </button>
            </div>
        </form>
    </section>

    <!-- PASO 2: Monitor de Progreso en Vivo -->
    <section class="ingest-card" id="step2Card" style="display: none;">
        <div class="progress-box">
            <div class="spinner-large"></div>
            <h3 id="progressTitle">Procesando documento...</h3>
            <p id="progressDetail" class="progress-detail">Subiendo archivo y ejecutando análisis con PyMuPDF...</p>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" id="progressBarFill"></div>
            </div>
            <div class="progress-steps-log" id="progressLog">
                <div class="log-item done">✓ Documento recibido en el servidor</div>
                <div class="log-item active" id="logExtract">⏳ Extrayendo texto y descartando cabeceras de página...</div>
                <div class="log-item" id="logNormalize">⏳ Normalizando Markdown y formato...</div>
            </div>
        </div>
    </section>

    <!-- PASO 3: Editor y Previsualización Dividida (Human-in-the-Loop) -->
    <section class="ingest-card full-width" id="step3Card" style="display: none;">
        <div class="editor-header">
            <div class="editor-header-info">
                <h2>Revisión del Apunte Extraído</h2>
                <p>Revisa el texto antes de confirmar su publicación. Puedes retocar el contenido, el título o añadir etiquetas clave.</p>
            </div>
            <div class="editor-header-stats" id="docStatsBadge">
                <span class="stat-pill" id="statPages">0 páginas</span>
                <span class="stat-pill" id="statWords">0 palabras</span>
                <span class="stat-pill" id="statChars">0 caracteres</span>
            </div>
        </div>

        <!-- Metadatos editables de la nota -->
        <div class="metadata-form-grid">
            <div class="form-group">
                <label for="editTitle">Título del Apunte <span class="required">*</span></label>
                <input type="text" id="editTitle" required placeholder="ej. Tema IV.13 La red Internet">
            </div>
            <div class="form-group">
                <label for="editOfficialTopic">Tema Oficial o Epígrafe</label>
                <input type="text" id="editOfficialTopic" placeholder="ej. IV.13 La red Internet">
            </div>
            <div class="form-group">
                <label for="editProcess">Proceso Asignado</label>
                <input type="text" id="editProcess" readonly class="input-readonly">
            </div>
            <div class="form-group">
                <label for="editTags">Etiquetas (separadas por coma)</label>
                <input type="text" id="editTags" placeholder="ej. redes, internet, ipv6, dns, tcp-ip">
            </div>
            <div class="form-group">
                <label for="editStatus">Estado</label>
                <select id="editStatus">
                    <option value="revisado" selected>Revisado (Listo para estudiar)</option>
                    <option value="borrador">Borrador (Requiere más trabajo)</option>
                </select>
            </div>
        </div>

        <!-- Barra de herramientas del editor -->
        <div class="editor-toolbar">
            <div class="toolbar-group">
                <button type="button" class="btn btn-sm" onclick="insertHeading('## ')">H2</button>
                <button type="button" class="btn btn-sm" onclick="insertHeading('### ')">H3</button>
                <button type="button" class="btn btn-sm" onclick="formatSelection('**', '**')"><strong>B</strong></button>
                <button type="button" class="btn btn-sm" onclick="formatSelection('*', '*')"><em>I</em></button>
                <button type="button" class="btn btn-sm" onclick="formatSelection('`', '`')"><code>&lt;/&gt;</code></button>
                <button type="button" class="btn btn-sm" onclick="insertList('- ')">• Lista</button>
                <button type="button" class="btn btn-sm" onclick="insertTable()">📊 Tabla</button>
            </div>
            <div class="toolbar-group">
                <button type="button" id="btnAiRefine" class="btn btn-sm btn-accent" onclick="handleAiRefine()">
                    <span>✨ Refinar con IA (Ollama)</span>
                </button>
                <button type="button" class="btn btn-sm btn-ghost" onclick="triggerManualPreview()">
                    <span>🔄 Actualizar Visor</span>
                </button>
            </div>
        </div>

        <!-- Panel dividido: Editor a la izquierda, Visor a la derecha -->
        <div class="split-editor">
            <div class="split-pane split-editor-pane">
                <div class="pane-header">
                    <span>Código Markdown Fuente</span>
                    <span id="editorWordCounter" class="pane-counter">0 palabras</span>
                </div>
                <textarea id="markdownEditor" class="markdown-textarea" placeholder="El texto extraído se cargará aquí..." oninput="handleEditorInput()"></textarea>
            </div>

            <div class="split-pane split-preview-pane">
                <div class="pane-header">
                    <span>Vista Previa Renderizada (Study Assistant)</span>
                    <span class="preview-badge">Render Real</span>
                </div>
                <div id="previewPane" class="preview-content note-body">
                    <p class="preview-placeholder">Escribe o procesa un documento para ver el formato final en vivo...</p>
                </div>
            </div>
        </div>

        <!-- Barra de acciones inferiores -->
        <div class="editor-footer-actions">
            <button type="button" class="btn btn-secondary" onclick="resetToStep1()">
                <span>← Descartar y Cargar Otro</span>
            </button>
            <button type="button" id="btnPublish" class="btn btn-success btn-large" onclick="handlePublish()">
                <span>🚀 Publicar en la Base de Conocimiento</span>
            </button>
        </div>
    </section>

    <!-- PASO 4: Pantalla de Éxito y Enlaces de Acción -->
    <section class="ingest-card" id="step4Card" style="display: none;">
        <div class="success-box">
            <div class="success-icon">🎉</div>
            <h2>¡Apunte publicado correctamente!</h2>
            <p class="success-message">El documento se ha guardado en la estructura oficial de conocimiento y el índice ha sido reconstruido automáticamente.</p>

            <div class="published-details-card">
                <div class="detail-row">
                    <span class="detail-label">Título:</span>
                    <strong class="detail-value" id="publishedTitle">-</strong>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Identificador (ID):</span>
                    <code class="detail-value" id="publishedId">-</code>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Ubicación física:</span>
                    <code class="detail-value" id="publishedPath">-</code>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Estado de sincronización:</span>
                    <span class="badge badge-success">✓ Índice knowledge_index.json actualizado</span>
                </div>
            </div>

            <div class="success-actions">
                <a id="linkViewNote" href="#" class="btn btn-primary btn-large">
                    <span>📖 Ver Apunte en StudyAssistant</span>
                </a>
                <a id="linkPracticeTest" href="http://localhost:8080" class="btn btn-accent btn-large" target="_blank" rel="noopener noreferrer">
                    <span>📝 Practicar Test en Preparador TAI</span>
                </a>
                <button type="button" class="btn btn-secondary" onclick="resetToStep1()">
                    <span>➕ Añadir Otra Fuente</span>
                </button>
            </div>
        </div>
    </section>
</div>

<script>
let currentExtractedData = null;
let previewDebounceTimer = null;

// Inicialización de eventos Drag & Drop
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('pdfFileInput');
const fileBadge = document.getElementById('fileSelectedBadge');
const fileNameDisplay = document.getElementById('fileNameDisplay');
const fileSizeDisplay = document.getElementById('fileSizeDisplay');

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('is-dragover');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('is-dragover');
    });
});

dropZone.addEventListener('drop', (e) => {
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        updateFileDisplay();
    }
});

fileInput.addEventListener('change', updateFileDisplay);

function updateFileDisplay() {
    if (fileInput.files && fileInput.files.length > 0) {
        const file = fileInput.files[0];
        fileNameDisplay.textContent = file.name;
        const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
        fileSizeDisplay.textContent = sizeMb + ' MB';
        fileBadge.style.display = 'inline-flex';
    } else {
        fileBadge.style.display = 'none';
    }
}

function handleProcessChange(select) {
    const customGroup = document.getElementById('customProcessGroup');
    const customInput = document.getElementById('customProcessInput');
    if (select.value === '__new__') {
        customGroup.style.display = 'block';
        customInput.required = true;
        customInput.focus();
    } else {
        customGroup.style.display = 'none';
        customInput.required = false;
    }
}

function setStep(stepNumber) {
    const steps = [1, 2, 3, 4];
    steps.forEach(s => {
        const stepper = document.getElementById('stepperStep' + s);
        const card = document.getElementById('step' + s + 'Card');
        if (s < stepNumber) {
            stepper.className = 'step-item completed';
        } else if (s === stepNumber) {
            stepper.className = 'step-item active';
        } else {
            stepper.className = 'step-item';
        }
        if (card) {
            card.style.display = (s === stepNumber) ? 'block' : 'none';
        }
    });
}

// 1. Extraer y procesar PDF
async function handleExtract(e) {
    e.preventDefault();
    if (!fileInput.files || fileInput.files.length === 0) {
        alert('Por favor, selecciona un archivo PDF para continuar.');
        return;
    }

    const processSelect = document.getElementById('processSelect');
    let processSlug = processSelect.value;
    if (processSlug === '__new__') {
        processSlug = document.getElementById('customProcessInput').value.trim();
        if (!processSlug) {
            alert('Por favor, indica el identificador del nuevo proceso selectivo.');
            return;
        }
    }

    setStep(2);
    const formData = new FormData();
    formData.append('pdf_file', fileInput.files[0]);
    formData.append('normalize', document.getElementById('optNormalize').checked ? 'true' : 'false');

    const progressBar = document.getElementById('progressBarFill');
    progressBar.style.width = '30%';

    try {
        const response = await fetch('ingest.php?action=extract', {
            method: 'POST',
            body: formData
        });

        progressBar.style.width = '75%';
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        progressBar.style.width = '100%';
        currentExtractedData = data;
        currentExtractedData.process_slug = processSlug;

        // Cargar en el editor (Paso 3)
        loadIntoEditor(data, processSlug);
        setStep(3);
    } catch (err) {
        alert('Error en la extracción: ' + err.message);
        setStep(1);
    }
}

function loadIntoEditor(data, processSlug) {
    document.getElementById('editTitle').value = data.detected_title || '';
    document.getElementById('editOfficialTopic').value = data.official_topic || data.detected_title || '';
    document.getElementById('editProcess').value = processSlug;

    // Sugerir etiquetas desde los títulos detectados
    let suggestedTags = [];
    if (data.headings && data.headings.length > 0) {
        data.headings.slice(0, 5).forEach(h => {
            const cleanH = h.replace(/^[0-9\.\-\s]+/, '').trim().toLowerCase();
            if (cleanH && cleanH.length > 3 && cleanH.length < 30) {
                suggestedTags.push(cleanH);
            }
        });
    }
    document.getElementById('editTags').value = suggestedTags.slice(0, 4).join(', ');

    // Estadísticas
    document.getElementById('statPages').textContent = (data.page_count || 1) + ' páginas';
    document.getElementById('statWords').textContent = (data.stats.word_count || 0) + ' palabras';
    document.getElementById('statChars').textContent = (data.stats.char_count || 0) + ' caracteres';

    // Contenido en textarea
    const textarea = document.getElementById('markdownEditor');
    textarea.value = data.markdown || '';
    updateEditorWordCounter();

    // Renderizar vista previa inicial
    renderPreview(textarea.value);
}

function handleEditorInput() {
    updateEditorWordCounter();
    clearTimeout(previewDebounceTimer);
    previewDebounceTimer = setTimeout(() => {
        renderPreview(document.getElementById('markdownEditor').value);
    }, 400);
}

function updateEditorWordCounter() {
    const text = document.getElementById('markdownEditor').value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    document.getElementById('editorWordCounter').textContent = words + ' palabras';
}

function triggerManualPreview() {
    renderPreview(document.getElementById('markdownEditor').value);
}

async function renderPreview(markdown) {
    const previewPane = document.getElementById('previewPane');
    try {
        const response = await fetch('ingest.php?action=preview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ markdown: markdown })
        });
        const data = await response.json();
        if (data.html) {
            previewPane.innerHTML = data.html;
            // Re-ejecutar MathJax si está presente
            if (window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise([previewPane]).catch(() => {});
            }
        }
    } catch (err) {
        console.error('Error al actualizar preview:', err);
    }
}

// 2. Refinado con IA (Ollama)
async function handleAiRefine() {
    const textarea = document.getElementById('markdownEditor');
    const originalText = textarea.value;
    if (!originalText.trim()) {
        alert('No hay contenido para refinar.');
        return;
    }

    const btnAi = document.getElementById('btnAiRefine');
    btnAi.disabled = true;
    const origHtml = btnAi.innerHTML;
    btnAi.innerHTML = '<span>⏳ Refinando con Ollama...</span>';

    try {
        const response = await fetch('ingest.php?action=refine', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                markdown: originalText,
                instructions: 'Asegura tablas limpias, une párrafos partidos y conserva todos los acrónimos y artículos legales.'
            })
        });

        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }

        if (data.refined_markdown) {
            textarea.value = data.refined_markdown;
            updateEditorWordCounter();
            renderPreview(data.refined_markdown);
            alert('¡Contenido refinado con IA con éxito!');
        }
    } catch (err) {
        alert('Aviso de refinado IA: ' + err.message + '\n\nPuedes continuar revisando y publicar directamente.');
    } finally {
        btnAi.disabled = false;
        btnAi.innerHTML = origHtml;
    }
}

// 3. Publicar la nota en la Base de Conocimiento
async function handlePublish() {
    const title = document.getElementById('editTitle').value.trim();
    if (!title) {
        alert('Por favor, indica un título para el apunte.');
        document.getElementById('editTitle').focus();
        return;
    }

    const officialTopic = document.getElementById('editOfficialTopic').value.trim();
    const processSlug = document.getElementById('editProcess').value.trim();
    const rawTags = document.getElementById('editTags').value.trim();
    const status = document.getElementById('editStatus').value;
    const markdownBody = document.getElementById('markdownEditor').value;
    const source = document.getElementById('sourceInput').value.trim() || 'cetic';

    const tags = rawTags.split(',').map(t => t.trim()).filter(t => t.length > 0);

    const btnPublish = document.getElementById('btnPublish');
    btnPublish.disabled = true;
    btnPublish.innerHTML = '<span>⏳ Publicando y re-indexando...</span>';

    try {
        const payload = {
            process_slug: processSlug,
            title: title,
            official_topic: officialTopic || title,
            markdown_body: markdownBody,
            tags: tags,
            status: status,
            source: source
        };

        const response = await fetch('ingest.php?action=publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.error) {
            throw new Error(result.error);
        }

        // Mostrar pantalla de éxito (Paso 4)
        document.getElementById('publishedTitle').textContent = title;
        document.getElementById('publishedId').textContent = result.note_id;
        document.getElementById('publishedPath').textContent = result.file_path;
        document.getElementById('linkViewNote').href = result.note_url;

        setStep(4);
    } catch (err) {
        alert('Error al publicar: ' + err.message);
    } finally {
        btnPublish.disabled = false;
        btnPublish.innerHTML = '<span>🚀 Publicar en la Base de Conocimiento</span>';
    }
}

function resetToStep1() {
    document.getElementById('ingestForm').reset();
    document.getElementById('fileSelectedBadge').style.display = 'none';
    document.getElementById('customProcessGroup').style.display = 'none';
    currentExtractedData = null;
    setStep(1);
}

// Utilidades del editor
function insertHeading(prefix) {
    const ta = document.getElementById('markdownEditor');
    const start = ta.selectionStart;
    ta.value = ta.value.substring(0, start) + '\n' + prefix + ta.value.substring(start);
    handleEditorInput();
    ta.focus();
}

function formatSelection(prefix, suffix) {
    const ta = document.getElementById('markdownEditor');
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const sel = ta.value.substring(start, end) || 'texto';
    ta.value = ta.value.substring(0, start) + prefix + sel + suffix + ta.value.substring(end);
    handleEditorInput();
    ta.focus();
}

function insertList(prefix) {
    const ta = document.getElementById('markdownEditor');
    const start = ta.selectionStart;
    ta.value = ta.value.substring(0, start) + '\n' + prefix + 'Elemento' + ta.value.substring(start);
    handleEditorInput();
    ta.focus();
}

function insertTable() {
    const ta = document.getElementById('markdownEditor');
    const start = ta.selectionStart;
    const tableTemplate = '\n| Columna 1 | Columna 2 | Columna 3 |\n|-----------|-----------|-----------|\n| Dato 1    | Dato 2    | Dato 3    |\n';
    ta.value = ta.value.substring(0, start) + tableTemplate + ta.value.substring(start);
    handleEditorInput();
    ta.focus();
}
</script>

<?php require_once __DIR__ . '/includes/footer.php'; ?>

