<?php

declare(strict_types=1);

namespace StudyAssistant\Navigation;

/**
 * Generador y renderizador del Índice de Contenidos (Table of Contents - TOC).
 * Construye una estructura arbórea jerárquica (h2 -> h3 -> h4)
 * y emite HTML accesible con soporte para acordeones colapsables (<details><summary>).
 */
class TableOfContents
{
    /**
     * Construye un árbol jerárquico a partir de la lista plana de encabezados.
     *
     * @param list<array{level: int, text: string, slug?: string}> $headings
     * @return list<array{heading: array, children: array}>
     */
    public function buildTree(array $headings): array
    {
        $tree = [];
        $stack = [];

        foreach ($headings as $h) {
            $level = (int)($h['level'] ?? 0);
            if ($level < 2 || $level > 4) {
                continue;
            }

            $node = ['heading' => $h, 'children' => []];

            while (!empty($stack) && (int)($stack[count($stack) - 1]['heading']['level'] ?? 0) >= $level) {
                array_pop($stack);
            }

            if (empty($stack)) {
                $tree[] = &$node;
            } else {
                $stack[count($stack) - 1]['children'][] = &$node;
            }

            $stack[] = &$node;
            unset($node);
        }

        return $tree;
    }

    /**
     * Renderiza el HTML del árbol del TOC con <details><summary> para niveles con hijos.
     *
     * @param list<array{heading: array, children: array}> $tree
     */
    public function renderTree(array $tree): string
    {
        if (empty($tree)) {
            return '';
        }

        $html = '<ul class="nested-toc-list">';
        foreach ($tree as $node) {
            $h = $node['heading'];
            $children = $node['children'] ?? [];
            $level = (int)($h['level'] ?? 2);
            $anchor = htmlspecialchars((string)($h['anchor'] ?? ($h['slug'] ?? '')), ENT_QUOTES, 'UTF-8');
            $text = htmlspecialchars((string)($h['text'] ?? ''), ENT_QUOTES, 'UTF-8');

            $html .= '<li class="toc-item level-' . $level . '">';

            if (!empty($children)) {
                $html .= '<details open class="toc-details">';
                $html .= '<summary class="toc-summary">';
                $html .= '<a href="#' . $anchor . '" onclick="event.stopPropagation()">' . $text . '</a>';
                $html .= '</summary>';
                $html .= $this->renderTree($children);
                $html .= '</details>';
            } else {
                $html .= '<div class="toc-link-wrapper">';
                $html .= '<a href="#' . $anchor . '">' . $text . '</a>';
                $html .= '</div>';
            }

            $html .= '</li>';
        }
        $html .= '</ul>';

        return $html;
    }

    /**
     * Renderiza directamente un listado plano de encabezados a su HTML correspondiente.
     *
     * @param list<array{level: int, text: string, anchor?: string, slug?: string}> $headings
     */
    public function render(array $headings): string
    {
        $tree = $this->buildTree($headings);
        return $this->renderTree($tree);
    }
}
