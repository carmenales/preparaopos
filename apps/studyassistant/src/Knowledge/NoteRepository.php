<?php

declare(strict_types=1);

namespace StudyAssistant\Knowledge;

/**
 * Repositorio de acceso a datos y metadatos de la Base de Conocimiento.
 * Maneja la carga del índice JSON, búsqueda, filtrado, resolución de rutas
 * y cálculos de navegación secuencial.
 */
class NoteRepository
{
    private static ?self $instance = null;
    private ?string $customIndexPath;
    private ?array $indexCache = null;
    private array $titlesCache = [];

    public function __construct(?string $customIndexPath = null)
    {
        $this->customIndexPath = $customIndexPath;
    }

    public static function getInstance(?string $customIndexPath = null): self
    {
        if (self::$instance === null || $customIndexPath !== null) {
            self::$instance = new self($customIndexPath);
        }
        return self::$instance;
    }

    public function getProjectBasePath(): string|false
    {
        return realpath(__DIR__ . '/../../../../');
    }

    public function getAppBasePath(): string|false
    {
        return realpath(__DIR__ . '/../../');
    }

    public function getIndexPath(): string
    {
        if ($this->customIndexPath !== null) {
            return $this->customIndexPath;
        }
        return $this->getAppBasePath() . '/data/knowledge_index.json';
    }

    /**
     * Carga el índice de notas con almacenamiento en caché en memoria.
     *
     * @return array<int, array<string, mixed>>
     */
    public function loadIndex(): array
    {
        if ($this->indexCache !== null) {
            return $this->indexCache;
        }

        $indexPath = $this->getIndexPath();
        if (!is_file($indexPath)) {
            $this->indexCache = [];
            return [];
        }

        $raw = file_get_contents($indexPath);
        $data = json_decode((string)$raw, true);

        if (isset($data['notes']) && is_array($data['notes'])) {
            $this->indexCache = $data['notes'];
            return $this->indexCache;
        }

        $this->indexCache = [];
        return [];
    }

    /**
     * Alias para loadIndex.
     */
    public function getAll(): array
    {
        return $this->loadIndex();
    }

    /**
     * Busca una nota por su identificador único.
     */
    public function find(string $id): ?array
    {
        return $this->findById($id);
    }

    /**
     * Busca una nota por su identificador único (con soporte opcional de subconjunto de notas).
     */
    public function findById(string $id, ?array $notes = null): ?array
    {
        $notes = $notes ?? $this->loadIndex();
        foreach ($notes as $note) {
            if ((string)($note['id'] ?? '') === $id) {
                return $note;
            }
        }
        return null;
    }

    /**
     * Resuelve la ruta absoluta del archivo Markdown asociado a una nota.
     * Tolera rutas relativas portables ('knowledge/processes/...'), rutas absolutas del sistema,
     * y prefijos de contenedor Docker, protegiendo estrictamente contra Path Traversal.
     */
    public function getAbsolutePath(array $note): ?string
    {
        $projectBasePath = $this->getProjectBasePath();
        $path = $note['path'] ?? null;

        if ($projectBasePath === false || !$path) {
            return null;
        }

        $knowledgeBasePath = realpath($projectBasePath . '/knowledge');
        if ($knowledgeBasePath === false) {
            return null;
        }

        $candidate = null;

        // 1. Ruta absoluta que existe directamente
        if (is_file($path)) {
            $candidate = realpath($path);
        }

        // 2. Ruta relativa respecto a la raíz del proyecto
        if ($candidate === null) {
            $relTry = $projectBasePath . '/' . ltrim($path, '/\\');
            if (is_file($relTry)) {
                $candidate = realpath($relTry);
            }
        }

        // 3. Ruta de contenedor Docker con prefijo antes de 'knowledge/'
        if ($candidate === null) {
            $normPath = str_replace('\\', '/', $path);
            $pos = strpos($normPath, 'knowledge/');
            if ($pos !== false) {
                $relKnowledge = substr($normPath, $pos);
                $relTry = $projectBasePath . '/' . $relKnowledge;
                if (is_file($relTry)) {
                    $candidate = realpath($relTry);
                }
            }
        }

        if ($candidate === false || $candidate === null) {
            return null;
        }

        // Validación estricta de Path Traversal
        if (strpos($candidate, $knowledgeBasePath) !== 0) {
            return null;
        }

        return $candidate;
    }

    /**
     * Filtra notas por texto de búsqueda, etiqueta, proceso y estado.
     *
     * @param list<array<string, mixed>>|null $notes Subconjunto opcional de notas a filtrar.
     * @return list<array<string, mixed>>
     */
    public function filter(string $query = '', string $tag = '', string $process = '', string $status = '', ?array $notes = null): array
    {
        $notes = $notes ?? $this->loadIndex();
        $query = trim($query);
        $tag = trim($tag);
        $process = trim($process);
        $status = trim($status);

        return array_values(array_filter($notes, function (array $note) use ($query, $tag, $process, $status): bool {
            if ($status !== '' && (string)($note['status'] ?? '') !== $status) {
                return false;
            }

            if ($tag !== '' && !in_array($tag, $note['tags'] ?? [], true)) {
                return false;
            }

            if ($process !== '' && !in_array($process, $note['processes'] ?? [], true)) {
                return false;
            }

            if ($query !== '') {
                $searchBlob = implode(' ', [
                    $note['title'] ?? '',
                    $note['official_topic'] ?? '',
                    $note['excerpt'] ?? '',
                    $note['content_text'] ?? '',
                    implode(' ', $note['tags'] ?? []),
                    implode(' ', $note['processes'] ?? []),
                ]);

                if (!$this->containsText($searchBlob, $query)) {
                    return false;
                }
            }

            return true;
        }));
    }

    /**
     * Obtiene todas las notas asociadas a un proceso selectivo determinado.
     *
     * @param string $process Slug del proceso selectivo.
     * @param list<array<string, mixed>>|null $notes Subconjunto opcional de notas.
     * @return list<array<string, mixed>>
     */
    public function getByProcess(string $process, ?array $notes = null): array
    {
        $notes = $notes ?? $this->loadIndex();
        $process = trim($process);
        if ($process === '') {
            return [];
        }

        return array_values(array_filter($notes, static function (array $n) use ($process): bool {
            return in_array($process, $n['processes'] ?? [], true);
        }));
    }

    /**
     * Comprobación insensible a mayúsculas y acentos.
     */
    public function containsText(string $haystack, string $needle): bool
    {
        if ($needle === '') {
            return true;
        }

        if (function_exists('mb_strtolower') && function_exists('mb_strpos')) {
            return mb_strpos(
                mb_strtolower($haystack, 'UTF-8'),
                mb_strtolower($needle, 'UTF-8'),
                0,
                'UTF-8'
            ) !== false;
        }

        return stripos($haystack, $needle) !== false;
    }

    /**
     * Recolecta valores únicos ordenados naturalmente para facetas.
     *
     * @param list<array<string, mixed>>|null $notes
     * @return list<string>
     */
    public function collectUnique(string $key, ?array $notes = null): array
    {
        $notes = $notes ?? $this->loadIndex();
        $values = [];

        foreach ($notes as $note) {
            $items = $note[$key] ?? [];

            if (!is_array($items)) {
                $items = [$items];
            }

            foreach ($items as $item) {
                if ($item !== null && $item !== '') {
                    $values[(string)$item] = (string)$item;
                }
            }
        }

        natcasesort($values);
        return array_values($values);
    }

    /**
     * Recolecta estados únicos ordenados.
     *
     * @param list<array<string, mixed>>|null $notes
     * @return list<string>
     */
    public function collectStatuses(?array $notes = null): array
    {
        $notes = $notes ?? $this->loadIndex();
        $values = [];

        foreach ($notes as $note) {
            $status = (string)($note['status'] ?? '');
            if ($status !== '') {
                $values[$status] = $status;
            }
        }

        natcasesort($values);
        return array_values($values);
    }

    /**
     * Ordena notas secuencialmente por tema oficial, id y título.
     */
    public function sortSequentially(array &$notes): void
    {
        usort($notes, static function ($a, $b): int {
            $topicA = trim((string)($a['official_topic'] ?? ''));
            $topicB = trim((string)($b['official_topic'] ?? ''));
            if ($topicA !== '' && $topicB !== '') {
                return strnatcasecmp($topicA, $topicB);
            }
            $idA = (string)($a['id'] ?? '');
            $idB = (string)($b['id'] ?? '');
            if ($idA !== '' && $idB !== '') {
                return strnatcasecmp($idA, $idB);
            }
            return strnatcasecmp((string)($a['title'] ?? ''), (string)($b['title'] ?? ''));
        });
    }

    /**
     * Normaliza los temas de práctica para conectar con preparadortai.
     *
     * @return list<string>
     */
    public function extractPracticeTopics(array $note): array
    {
        $practiceTopics = [];

        if (!empty($note['practice']['topics']) && is_array($note['practice']['topics'])) {
            foreach ($note['practice']['topics'] as $topic) {
                $topic = trim((string)$topic);
                if ($topic !== '') {
                    $practiceTopics[] = $topic;
                }
            }
        }

        if (empty($practiceTopics) && !empty($note['tags']) && is_array($note['tags'])) {
            foreach ($note['tags'] as $tag) {
                $tag = trim((string)$tag);
                if ($tag !== '') {
                    $practiceTopics[] = $tag;
                }
            }
        }

        if (empty($practiceTopics) && !empty($note['official_topic'])) {
            if (preg_match('/Tema\s+([0-9]+)/i', (string)$note['official_topic'], $matches)) {
                $practiceTopics[] = trim($matches[1]);
            } else {
                $practiceTopics[] = trim((string)$note['official_topic']);
            }
        }

        return array_values(array_unique(array_filter($practiceTopics, static function ($topic): bool {
            return trim((string)$topic) !== '';
        })));
    }

    /**
     * Alias para extractPracticeTopics.
     *
     * @return list<string>
     */
    public function normalizePracticeTopics(array $note): array
    {
        return $this->extractPracticeTopics($note);
    }

    /**
     * Formatea el título legible de un proceso a partir de su README.md o de su slug.
     */
    public function formatProcessTitle(string $slug): string
    {
        $slug = trim($slug);
        if ($slug === '' || $slug === 'Sin proceso') {
            return 'Sin proceso asignado';
        }

        if (isset($this->titlesCache[$slug])) {
            return $this->titlesCache[$slug];
        }

        $projectPath = $this->getProjectBasePath();
        if ($projectPath) {
            $processDir = $projectPath . '/knowledge/processes/' . $slug;
            foreach (['README.md', 'readme.md'] as $readmeName) {
                $readmePath = $processDir . '/' . $readmeName;
                if (is_file($readmePath)) {
                    $handle = @fopen($readmePath, 'r');
                    if ($handle) {
                        while (($line = fgets($handle)) !== false) {
                            $line = trim($line);
                            if (strpos($line, '# ') === 0) {
                                $title = trim(substr($line, 2));
                                if ($title !== '') {
                                    fclose($handle);
                                    $this->titlesCache[$slug] = $title;
                                    return $title;
                                }
                            }
                        }
                        fclose($handle);
                    }
                }
            }
        }

        $formatted = $this->prettifySlug($slug);
        $this->titlesCache[$slug] = $formatted;
        return $formatted;
    }

    /**
     * Embellece un slug convirtiéndolo en títulos legibles con acentos y conectores.
     */
    public function prettifySlug(string $slug): string
    {
        $segments = explode('/', $slug);
        $formattedSegments = [];
        $connectors = ['de', 'del', 'la', 'las', 'el', 'los', 'en', 'y', 'a', 'por', 'para', 'con', 'e'];
        $accents = [
            'administracion' => 'Administración',
            'innovacion' => 'Innovación',
            'transformacion' => 'Transformación',
            'informatica' => 'Informática',
            'gestion' => 'Gestión',
            'tecnico' => 'Técnico',
            'comunicacion' => 'Comunicación',
        ];

        foreach ($segments as $segment) {
            $words = preg_split('/[\s\-_]+/', trim($segment));
            $formattedWords = [];

            foreach ($words as $i => $word) {
                $lower = function_exists('mb_strtolower') ? mb_strtolower($word, 'UTF-8') : strtolower($word);
                if ($lower === '') {
                    continue;
                }

                if (isset($accents[$lower])) {
                    $formattedWords[] = $accents[$lower];
                } elseif ($i > 0 && in_array($lower, $connectors, true)) {
                    $formattedWords[] = $lower;
                } elseif (strlen($lower) <= 3 || preg_match('/^[a-z][0-9]$/i', $lower)) {
                    $formattedWords[] = function_exists('mb_strtoupper') ? mb_strtoupper($lower, 'UTF-8') : strtoupper($lower);
                } else {
                    $formattedWords[] = function_exists('mb_convert_case')
                        ? mb_convert_case($lower, MB_CASE_TITLE, 'UTF-8')
                        : ucfirst($lower);
                }
            }

            if (!empty($formattedWords)) {
                $formattedSegments[] = implode(' ', $formattedWords);
            }
        }

        return implode(' › ', $formattedSegments) ?: $slug;
    }

    /**
     * Estima el tiempo de lectura de una nota.
     */
    public function estimateReadingTime(array $note): string
    {
        $text = $note['content_text'] ?? ($note['excerpt'] ?? '');
        $charCount = function_exists('mb_strlen') ? mb_strlen((string)$text, 'UTF-8') : strlen((string)$text);
        $minutes = max(1, (int)ceil($charCount / 800));
        return "~{$minutes} min";
    }

    /**
     * Devuelve la clase CSS del badge de estado.
     */
    public function getStatusBadgeClass(string $status): string
    {
        $status = strtolower(trim($status));
        if (in_array($status, ['revisado', 'publicado', 'completo', 'listo'], true)) {
            return 'badge-status-revisado';
        }
        if (in_array($status, ['borrador', 'en-revision', 'draft'], true)) {
            return 'badge-status-borrador';
        }
        return 'badge-status-default';
    }

    /**
     * Alias para getStatusBadgeClass.
     */
    public function statusBadgeClass(string $status): string
    {
        return $this->getStatusBadgeClass($status);
    }

    /**
     * Carga el registro de procesos desde el índice JSON si existe.
     *
     * @return array<int, array<string, mixed>>
     */
    public function loadProcessesRegistry(): array
    {
        $indexPath = $this->getIndexPath();
        if (is_file($indexPath)) {
            $raw = file_get_contents($indexPath);
            $data = json_decode((string)$raw, true);
            if (!empty($data['processes']) && is_array($data['processes'])) {
                return $data['processes'];
            }
        }
        return [];
    }

    /**
     * Alias para loadProcessesRegistry.
     *
     * @return array<int, array<string, mixed>>
     */
    public function getProcessesRegistry(): array
    {
        return $this->loadProcessesRegistry();
    }
}
