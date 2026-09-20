<?php

declare(strict_types=1);

namespace StudyAssistant\Dashboard;

use StudyAssistant\Knowledge\NoteRepository;

/**
 * Calculador de métricas y agregaciones del Dashboard y Process Hub.
 * Extrae y estructura conteos globales, estados de revisión por proceso
 * y chips de filtros activos.
 */
class DashboardMetrics
{
    private array $notes;
    private array $processes;
    private array $tags;
    private NoteRepository $repository;

    private ?int $reviewedCount = null;
    private ?int $draftCount = null;
    private ?array $processSummaries = null;

    public function __construct(
        array $notes,
        array $processes,
        array $tags,
        ?NoteRepository $repository = null
    ) {
        $this->notes = $notes;
        $this->processes = $processes;
        $this->tags = $tags;
        $this->repository = $repository ?? NoteRepository::getInstance();
    }

    public static function fromRepository(?NoteRepository $repository = null): self
    {
        $repo = $repository ?? NoteRepository::getInstance();
        $notes = $repo->loadIndex();
        $processes = $repo->collectUnique('processes');
        $tags = $repo->collectUnique('tags');

        return new self($notes, $processes, $tags, $repo);
    }

    public function getTotalNotes(): int
    {
        return count($this->notes);
    }

    public function getTotalProcesses(): int
    {
        return count($this->processes);
    }

    public function getTotalTags(): int
    {
        return count($this->tags);
    }

    public function getReviewedCount(): int
    {
        if ($this->reviewedCount === null) {
            $this->calculateCounts();
        }
        return (int)$this->reviewedCount;
    }

    public function getDraftCount(): int
    {
        if ($this->draftCount === null) {
            $this->calculateCounts();
        }
        return (int)$this->draftCount;
    }

    private function calculateCounts(): void
    {
        $this->reviewedCount = 0;
        $this->draftCount = 0;

        foreach ($this->notes as $note) {
            $status = strtolower((string)($note['status'] ?? ''));
            if (in_array($status, ['revisado', 'publicado', 'completo', 'listo'], true)) {
                $this->reviewedCount++;
            } else {
                $this->draftCount++;
            }
        }
    }

    /**
     * Calcula los resúmenes agregados por proceso para el Process Hub.
     *
     * @return array<string, array{slug: string, title: string, total: int, reviewed: int, draft: int, tags: list<string>}>
     */
    public function getProcessSummaries(): array
    {
        if ($this->processSummaries !== null) {
            return $this->processSummaries;
        }

        $summaries = [];
        foreach ($this->processes as $procSlug) {
            $procNotes = array_filter($this->notes, static function (array $n) use ($procSlug): bool {
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

            $summaries[$procSlug] = [
                'slug' => $procSlug,
                'title' => $this->repository->formatProcessTitle($procSlug),
                'total' => $procTotal,
                'reviewed' => $procReviewed,
                'draft' => $procDraft,
                'tags' => $topTags,
            ];
        }

        $this->processSummaries = $summaries;
        return $summaries;
    }

    /**
     * Cuenta notas revisadas y en borrador para un subconjunto específico de notas.
     *
     * @param list<array<string, mixed>> $notesSubset
     * @return array{reviewed: int, draft: int}
     */
    public function countReviewedAndDraft(array $notesSubset): array
    {
        $reviewed = 0;
        $draft = 0;

        foreach ($notesSubset as $note) {
            $status = strtolower((string)($note['status'] ?? ''));
            if (in_array($status, ['revisado', 'publicado', 'completo', 'listo'], true)) {
                $reviewed++;
            } else {
                $draft++;
            }
        }

        return ['reviewed' => $reviewed, 'draft' => $draft];
    }

    /**
     * Construye la lista de chips de filtros activos con sus URLs de eliminación.
     *
     * @param array<string, mixed> $getParams
     * @return list<array{name: string, value: string, remove_url: string}>
     */
    public function buildActiveFilters(
        array $getParams,
        string $query,
        string $process,
        string $tag,
        string $status
    ): array {
        $activeFilters = [];

        if ($query !== '') {
            $params = $getParams;
            unset($params['q']);
            $activeFilters[] = [
                'name' => 'Búsqueda',
                'value' => $query,
                'remove_url' => 'index.php?' . http_build_query($params),
            ];
        }

        if ($process !== '') {
            $params = $getParams;
            unset($params['process']);
            $activeFilters[] = [
                'name' => 'Proceso',
                'value' => $this->repository->formatProcessTitle($process),
                'remove_url' => 'index.php?' . http_build_query($params),
            ];
        }

        if ($tag !== '') {
            $params = $getParams;
            unset($params['tag']);
            $activeFilters[] = [
                'name' => 'Etiqueta',
                'value' => $tag,
                'remove_url' => 'index.php?' . http_build_query($params),
            ];
        }

        if ($status !== '') {
            $params = $getParams;
            unset($params['status']);
            $activeFilters[] = [
                'name' => 'Estado',
                'value' => ucfirst($status),
                'remove_url' => 'index.php?' . http_build_query($params),
            ];
        }

        return $activeFilters;
    }
}

