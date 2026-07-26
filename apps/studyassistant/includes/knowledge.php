<?php

function sa_project_base_path() {
    return realpath(__DIR__ . '/../../..');
}

function sa_app_base_path() {
    return realpath(__DIR__ . '/..');
}

function sa_index_path() {
    return sa_app_base_path() . '/data/knowledge_index.json';
}

function sa_safe_text($value) {
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function sa_load_index() {
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

function sa_find_note_by_id($notes, $id) {
    foreach ($notes as $note) {
        if ((string)($note['id'] ?? '') === (string)$id) {
            return $note;
        }
    }

    return null;
}

function sa_note_absolute_path($note) {
    $projectBasePath = sa_project_base_path();
    $path = $note['path'] ?? '';

    if ($projectBasePath === false || $path === '') {
        return null;
    }

    $absolutePath = realpath($projectBasePath . '/' . $path);
    $knowledgeBasePath  = realpath($projectBasePath . '/knowledge');

    if ($absolutePath === false || $knowledgeBasePath  === false) {
        return null;
    }

    if (strpos($absolutePath, $knowledgeBasePath ) !== 0) {
        return null;
    }

    return $absolutePath;
}

function sa_contains_text($haystack, $needle) {
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

function sa_filter_notes($notes, $query, $tag, $process, $status) {
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

function sa_collect_unique($notes, $key) {
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

function sa_collect_statuses($notes) {
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

function sa_selected_attr($current, $value) {
    return (string)$current === (string)$value ? 'selected' : '';
}
