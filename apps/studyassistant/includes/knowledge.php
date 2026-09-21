<?php

declare(strict_types=1);

require_once __DIR__ . '/autoload.php';

use StudyAssistant\Knowledge\NoteRepository;
use StudyAssistant\Service\KnowledgeServiceClient;

/**
 * Facade procedural para mantener 100% de retrocompatibilidad con scripts existentes.
 * Todas las llamadas delegan directamente en las clases de StudyAssistant\.
 */

function sa_project_base_path(): ?string
{
    return NoteRepository::getInstance()->getProjectBasePath();
}

function sa_app_base_path(): string
{
    return NoteRepository::getInstance()->getAppBasePath();
}

function sa_index_path(): string
{
    return NoteRepository::getInstance()->getIndexPath();
}

function sa_safe_text(mixed $value): string
{
    return htmlspecialchars((string)($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function sa_load_index(): array
{
    return NoteRepository::getInstance()->getAll();
}

function sa_find_note_by_id(array $notes, mixed $id): ?array
{
    // Si la lista pasada es la misma que la del repositorio, usamos el lookup O(1)
    $repo = NoteRepository::getInstance();
    $found = $repo->findById((string)$id);
    if ($found !== null) {
        return $found;
    }

    // Fallback por si se pasa un subconjunto arbitrario de notas
    foreach ($notes as $note) {
        if ((string)($note['id'] ?? '') === (string)$id) {
            return $note;
        }
    }

    return null;
}

function sa_note_absolute_path(array $note): ?string
{
    return NoteRepository::getInstance()->getAbsolutePath($note);
}

function sa_contains_text(string $haystack, string $needle): bool
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

function sa_filter_notes(array $notes, mixed $query, mixed $tag, mixed $process, mixed $status): array
{
    return NoteRepository::getInstance()->filter(
        (string)($query ?? ''),
        (string)($tag ?? ''),
        (string)($process ?? ''),
        (string)($status ?? ''),
        $notes
    );
}

function sa_collect_unique(array $notes, string $key): array
{
    return NoteRepository::getInstance()->collectUnique($key, $notes);
}

function sa_collect_statuses(array $notes): array
{
    return NoteRepository::getInstance()->collectStatuses($notes);
}

function sa_selected_attr(mixed $current, mixed $value): string
{
    return (string)$current === (string)$value ? 'selected' : '';
}

function sa_normalize_practice_topics(array $note): array
{
    return NoteRepository::getInstance()->normalizePracticeTopics($note);
}

function sa_prettify_slug(string $slug): string
{
    return NoteRepository::getInstance()->prettifySlug($slug);
}

function sa_format_process_title(string $slug): string
{
    return NoteRepository::getInstance()->formatProcessTitle($slug);
}

function sa_estimate_reading_time(array $note): string
{
    return NoteRepository::getInstance()->estimateReadingTime($note);
}

function sa_status_badge_class(string $status): string
{
    return NoteRepository::getInstance()->statusBadgeClass($status);
}

function sa_sort_notes_sequentially(array &$notes): void
{
    NoteRepository::getInstance()->sortSequentially($notes);
}

function sa_knowledge_service_url(): string
{
    return (new KnowledgeServiceClient())->getBaseUrl();
}

function sa_load_processes_registry(): array
{
    return NoteRepository::getInstance()->getProcessesRegistry();
}

function build_nested_toc(array $headings): array
{
    return (new \StudyAssistant\Navigation\TableOfContents())->buildTree($headings);
}

function render_nested_toc(array $tree): string
{
    return (new \StudyAssistant\Navigation\TableOfContents())->renderTree($tree);
}
