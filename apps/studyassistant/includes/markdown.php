<?php

function sa_strip_frontmatter($markdown) {
    if (strpos($markdown, "---\n") !== 0) {
        return $markdown;
    }

    $end = strpos($markdown, "\n---", 4);

    if ($end === false) {
        return $markdown;
    }

    return ltrim(substr($markdown, $end + 4), "\n");
}

function sa_inline_markdown($text) {
    $text = htmlspecialchars((string)$text, ENT_QUOTES, 'UTF-8');

    $text = preg_replace('/`([^`]+)`/', '<code>$1</code>', $text);
    $text = preg_replace('/\*\*([^*]+)\*\*/', '<strong>$1</strong>', $text);
    $text = preg_replace('/\*([^*]+)\*/', '<em>$1</em>', $text);
    $text = preg_replace('/\[([^\]]+)\]\(([^)]+)\)/', '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>', $text);

    return $text;
}

function sa_render_table($lines) {
    $html = '<div class="table-wrapper"><table>';
    $headerRendered = false;

    foreach ($lines as $index => $line) {
        if ($index === 1 && preg_match('/^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/', $line)) {
            continue;
        }

        $cells = array_map('trim', explode('|', trim($line, '| ')));
        $tag = $headerRendered ? 'td' : 'th';
        $html .= '<tr>';

        foreach ($cells as $cell) {
            $html .= '<' . $tag . '>' . sa_inline_markdown($cell) . '</' . $tag . '>';
        }

        $html .= '</tr>';
        $headerRendered = true;
    }

    $html .= '</table></div>';

    return $html;
}

function sa_render_markdown($markdown) {
    $markdown = sa_strip_frontmatter($markdown);
    $lines = preg_split('/\R/', $markdown);
    $html = '';
    $paragraph = [];
    $inCode = false;
    $codeBuffer = [];
    $listOpen = false;
    $tableBuffer = [];

    $flushParagraph = function () use (&$html, &$paragraph) {
        if (!empty($paragraph)) {
            $html .= '<p>' . sa_inline_markdown(implode(' ', $paragraph)) . '</p>';
            $paragraph = [];
        }
    };

    $closeList = function () use (&$html, &$listOpen) {
        if ($listOpen) {
            $html .= '</ul>';
            $listOpen = false;
        }
    };

    $flushTable = function () use (&$html, &$tableBuffer) {
        if (!empty($tableBuffer)) {
            $html .= sa_render_table($tableBuffer);
            $tableBuffer = [];
        }
    };

    foreach ($lines as $line) {
        if (preg_match('/^```/', $line)) {
            $flushParagraph();
            $closeList();
            $flushTable();

            if ($inCode) {
                $html .= '<pre><code>' . htmlspecialchars(implode("\n", $codeBuffer), ENT_QUOTES, 'UTF-8') . '</code></pre>';
                $codeBuffer = [];
                $inCode = false;
            } else {
                $inCode = true;
            }

            continue;
        }

        if ($inCode) {
            $codeBuffer[] = $line;
            continue;
        }

        if (trim($line) === '') {
            $flushParagraph();
            $closeList();
            $flushTable();
            continue;
        }

        if (strpos(trim($line), '|') !== false && preg_match('/^\s*\|?.+\|.+\|?\s*$/', $line)) {
            $flushParagraph();
            $closeList();
            $tableBuffer[] = $line;
            continue;
        }

        $flushTable();

        if (preg_match('/^(#{1,6})\s+(.+)$/', $line, $matches)) {
            $flushParagraph();
            $closeList();
            $level = strlen($matches[1]);
            $text = trim($matches[2]);
            $slug = strtolower(preg_replace('/[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]+/u', '-', $text));
            $html .= '<h' . $level . ' id="' . htmlspecialchars($slug, ENT_QUOTES, 'UTF-8') . '">' . sa_inline_markdown($text) . '</h' . $level . '>';
            continue;
        }

        if (preg_match('/^\s*[-*]\s+(.+)$/', $line, $matches)) {
            $flushParagraph();

            if (!$listOpen) {
                $html .= '<ul>';
                $listOpen = true;
            }

            $html .= '<li>' . sa_inline_markdown($matches[1]) . '</li>';
            continue;
        }

        $paragraph[] = trim($line);
    }

    if ($inCode) {
        $html .= '<pre><code>' . htmlspecialchars(implode("\n", $codeBuffer), ENT_QUOTES, 'UTF-8') . '</code></pre>';
    }

    $flushParagraph();
    $closeList();
    $flushTable();

    return $html;
}
