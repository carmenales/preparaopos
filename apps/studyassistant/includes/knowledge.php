<?php

function sa_project_base_path()
{
    return realpath(__DIR__ . '/../../..');
}

function sa_app_base_path()
{
    return realpath(__DIR__ . '/..');
}

function sa_index_path()
{
    return sa_app_base_path() . '/data/knowledge_index.json';
}

function sa_safe_text($value)
{
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function sa_load_index()
{
    $indexPath = sa_index_path();

    if (!is_file($indexPath)) {
        return [];
    }

    $raw = file_get_contents($indexPath);
    $data = json_decode($raw, true);

    if (isset($data['notes']) && is_array($data['notes'])) {
        return $data['notes'];
    }

    return [];
}

function sa_find_note_by_id(array $notes, $id)
{
    foreach ($notes as $note) {
        if ((string)($note['id'] ?? '') === (string)$id) {
            return $note;
        }
    }

    return null;
}

function sa_note_absolute_path(array $note)
{
    $projectBasePath = sa_project_base_path();
    $path = $note['path'] ?? null;

    if ($projectBasePath === false || !$path) {
        return null;
    }

    $knowledgeBasePath = realpath($projectBasePath . '/knowledge');
    if ($knowledgeBasePath === false) {
        return null;
    }

    $candidate = null;

    if (is_file($path)) {
        $candidate = realpath($path);
    }

    if ($candidate === null) {
        $relTry = $projectBasePath . '/' . ltrim($path, '/\\');
        if (is_file($relTry)) {
            $candidate = realpath($relTry);
        }
    }

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

    if (strpos($candidate, $knowledgeBasePath) !== 0) {
        return null;
    }

    return $candidate;
}

function sa_contains_text($haystack, $needle)
{
    if ($needle === '') {
        return true;
    }

    if (function_exists('mb_strtolower') && function_exists('mb_strpos')) {
        return mb_strpos(
            mb_strtolower((string)$haystack, 'UTF-8'),
            mb_strtolower((string)$needle, 'UTF-8'),
            0,
            'UTF-8'
        ) !== false;
    }

    return stripos((string)$haystack, (string)$needle) !== false;
}

function sa_filter_notes(array $notes, $query, $tag, $process, $status)
{
    $query = trim((string)$query);
    $tag = trim((string)$tag);
    $process = trim((string)$process);
    $status = trim((string)$status);

    return array_values(array_filter($notes, function ($note) use ($query, $tag, $process, $status) {
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

            if (!sa_contains_text($searchBlob, $query)) {
                return false;
            }
        }

        return true;
    }));
}

function sa_collect_unique(array $notes, string $key)
{
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

function sa_collect_statuses(array $notes)
{
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

function sa_selected_attr($current, $value)
{
    return (string)$current === (string)$value ? 'selected' : '';
}

function sa_normalize_practice_topics(array $note): array
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

    $practiceTopics = array_values(array_unique(array_filter($practiceTopics, static function ($topic) {
        return trim((string)$topic) !== '';
    })));

    return $practiceTopics;
}

function sa_prettify_slug(string $slug): string
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

function sa_format_process_title(string $slug): string
{
    $slug = trim($slug);
    if ($slug === '' || $slug === 'Sin proceso') {
        return 'Sin proceso asignado';
    }

    static $titlesCache = [];
    if (isset($titlesCache[$slug])) {
        return $titlesCache[$slug];
    }

    $projectPath = sa_project_base_path();
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
                                $titlesCache[$slug] = $title;
                                return $title;
                            }
                        }
                    }
                    fclose($handle);
                }
            }
        }
    }

    $formatted = sa_prettify_slug($slug);
    $titlesCache[$slug] = $formatted;
    return $formatted;
}

function sa_estimate_reading_time(array $note): string
{
    $text = $note['content_text'] ?? ($note['excerpt'] ?? '');
    $charCount = function_exists('mb_strlen') ? mb_strlen((string)$text, 'UTF-8') : strlen((string)$text);
    $minutes = max(1, (int)ceil($charCount / 800));
    return "~{$minutes} min";
}

function sa_status_badge_class(string $status): string
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

function sa_sort_notes_sequentially(array &$notes): void
{
    usort($notes, static function ($a, $b) {
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

function sa_knowledge_service_url(): string
{
    return getenv('KNOWLEDGE_SERVICE_URL') ?: 'http://knowledge-service:8000';
}

function sa_load_processes_registry(): array
{
    $indexPath = sa_index_path();
    if (is_file($indexPath)) {
        $raw = file_get_contents($indexPath);
        $data = json_decode($raw, true);
        if (!empty($data['processes']) && is_array($data['processes'])) {
            return $data['processes'];
        }
    }
    return [];
}
