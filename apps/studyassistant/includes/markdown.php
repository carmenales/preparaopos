<?php

function sa_normalize_markdown($markdown) {
    $markdown = (string)$markdown;
    $markdown = preg_replace('/^\xEF\xBB\xBF/', '', $markdown);
    return str_replace(["\r\n", "\r"], "\n", $markdown);
}

function sa_strip_frontmatter($markdown) {
    $markdown = sa_normalize_markdown($markdown);

    if (preg_match('/\A---\s*\n.*?\n---\s*\n/s', $markdown, $matches)) {
        return substr($markdown, strlen($matches[0]));
    }

    return $markdown;
}

function sa_math_placeholder($key) {
    return '%%SA_MATH_' . $key . '%%';
}

function sa_extract_inline_math($text, &$mathBlocks) {
    return preg_replace_callback('/(?<!\\\\)\$([^$\n]+)(?<!\\\\)\$/', function ($matches) use (&$mathBlocks) {
        $key = count($mathBlocks);
        $mathBlocks[$key] = [
            'type' => 'inline',
            'content' => $matches[1],
        ];

        return sa_math_placeholder($key);
    }, (string)$text);
}

function sa_restore_math_placeholders($html, $mathBlocks) {
    foreach ($mathBlocks as $key => $math) {
        $placeholder = sa_math_placeholder($key);
        $formula = htmlspecialchars($math['content'], ENT_NOQUOTES, 'UTF-8');

        if ($math['type'] === 'inline') {
            $replacement = '<span class="math-inline">\\(' . $formula . '\\)</span>';
        } else {
            $replacement = '<div class="math-block">\\[' . $formula . '\\]</div>';
        }

        $html = str_replace($placeholder, $replacement, $html);
    }

    return $html;
}

function sa_inline_markdown($text) {
    $mathBlocks = [];
    $text = sa_extract_inline_math((string)$text, $mathBlocks);

    $html = htmlspecialchars($text, ENT_QUOTES, 'UTF-8');

    $html = preg_replace('/`([^`]+)`/', '<code>$1</code>', $html);
    $html = preg_replace('/\*\*([^*]+)\*\*/', '<strong>$1</strong>', $html);
    $html = preg_replace('/\*([^*]+)\*/', '<em>$1</em>', $html);
    $html = preg_replace('/\[([^\]]+)\]\(([^)]+)\)/', '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>', $html);

    return sa_restore_math_placeholders($html, $mathBlocks);
}

function sa_slugify_heading($text) {
    $text = trim((string)$text);
    $text = iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $text);
    $text = preg_replace('/[^\p{L}\p{N}]+/u', '-', $text);
    $text = trim($text, '-');

    return function_exists('mb_strtolower') ? mb_strtolower($text, 'UTF-8') : strtolower($text);
}

function sa_render_table($lines) {
    $html = '<div class="table-wrapper"><table>';
    $headerRendered = false;

    foreach ($lines as $index => $line) {
        if ($index === 1 && sa_is_table_separator($line)) {
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

function sa_has_pipe($line) {
    return strpos(trim((string)$line), '|') !== false;
}

function sa_is_table_separator($line) {
    return preg_match('/^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/', (string)$line);
}

function sa_is_table_start($lines, $index) {
    if (!isset($lines[$index + 1])) {
        return false;
    }

    return sa_has_pipe($lines[$index]) && sa_is_table_separator($lines[$index + 1]);
}

function sa_collect_table($lines, &$index) {
    $tableLines = [];

    while ($index < count($lines)) {
        $line = $lines[$index];

        if (trim($line) === '') {
            break;
        }

        if (!sa_has_pipe($line) && !sa_is_table_separator($line)) {
            break;
        }

        $tableLines[] = $line;
        $index++;
    }

    return sa_render_table($tableLines);
}

function sa_is_quiz_question_start($line) {
    return preg_match('/^\s*(?:\*\*)?Pregunta\s+([0-9]+)\.(?:\*\*)?\s*(.*)$/u', trim($line));
}

function sa_parse_answer_line($line) {
    $clean = trim($line);
    $clean = preg_replace('/^\*\*/', '', $clean);
    $clean = preg_replace('/\*\*/', '', $clean);

    if (!preg_match('/^Respuesta correcta:\s*(.+)$/u', $clean, $matches)) {
        return null;
    }

    return trim($matches[1]);
}

function sa_render_quiz_question($questionNumber, $questionText, $options, $answerText) {
    $html = '<section class="quiz-card">';
    $html .= '<div class="quiz-question-label">Pregunta ' . (int)$questionNumber . '</div>';
    $html .= '<div class="quiz-question-text">' . sa_inline_markdown($questionText) . '</div>';

    if (!empty($options)) {
        $html .= '<ol class="quiz-options" type="A">';

        foreach ($options as $option) {
            $html .= '<li>' . sa_inline_markdown($option) . '</li>';
        }

        $html .= '</ol>';
    }

    if ($answerText !== '') {
        $html .= '<details class="quiz-answer">';
        $html .= '<summary>Mostrar respuesta y explicación</summary>';
        $html .= '<div>' . sa_inline_markdown($answerText) . '</div>';
        $html .= '</details>';
    }

    $html .= '</section>';

    return $html;
}

function sa_collect_quiz_question($lines, &$index) {
    $line = trim($lines[$index]);
    preg_match('/^\s*(?:\*\*)?Pregunta\s+([0-9]+)\.(?:\*\*)?\s*(.*)$/u', $line, $matches);

    $questionNumber = (int)$matches[1];
    $questionParts = [];
    $initialText = trim($matches[2]);

    if ($initialText !== '') {
        $questionParts[] = $initialText;
    }

    $options = [];
    $answerText = '';
    $currentOptionIndex = null;
    $index++;

    while ($index < count($lines)) {
        $currentLine = trim($lines[$index]);

        if ($currentLine === '') {
            $index++;
            continue;
        }

        if (preg_match('/^#{1,6}\s+/', $currentLine) || sa_is_quiz_question_start($currentLine)) {
            break;
        }

        $parsedAnswer = sa_parse_answer_line($currentLine);

        if ($parsedAnswer !== null) {
            $answerText = $parsedAnswer;
            $index++;
            continue;
        }

        if ($answerText !== '') {
            $answerText .= ' ' . $currentLine;
            $index++;
            continue;
        }

        if (preg_match('/^([A-D])\.\s+(.+)$/u', $currentLine, $optionMatches)) {
            $options[] = trim($optionMatches[2]);
            $currentOptionIndex = count($options) - 1;
            $index++;
            continue;
        }

        if ($currentOptionIndex !== null) {
            $options[$currentOptionIndex] .= ' ' . $currentLine;
        } else {
            $questionParts[] = $currentLine;
        }

        $index++;
    }

    return sa_render_quiz_question(
        $questionNumber,
        trim(implode(' ', $questionParts)),
        $options,
        $answerText
    );
}

function sa_parse_list_marker($line) {
    if (preg_match('/^\s*([0-9]+)\.\s+(.+)$/u', $line, $matches)) {
        return [
            'type' => 'ol',
            'number' => (int)$matches[1],
            'content' => trim($matches[2]),
        ];
    }

    if (preg_match('/^\s*[-*]\s+(.+)$/u', $line, $matches)) {
        return [
            'type' => 'ul',
            'number' => null,
            'content' => trim($matches[1]),
        ];
    }

    return null;
}

function sa_next_non_empty_index($lines, $index) {
    for ($i = $index; $i < count($lines); $i++) {
        if (trim($lines[$i]) !== '') {
            return $i;
        }
    }

    return null;
}

function sa_collect_list($lines, &$index) {
    $firstMarker = sa_parse_list_marker($lines[$index]);

    if ($firstMarker === null) {
        return '';
    }

    $type = $firstMarker['type'];
    $start = $firstMarker['number'];
    $items = [];
    $current = null;

    while ($index < count($lines)) {
        $line = $lines[$index];
        $trimmed = trim($line);

        if ($trimmed === '') {
            $nextIndex = sa_next_non_empty_index($lines, $index + 1);

            if ($nextIndex === null) {
                $index++;
                break;
            }

            $nextMarker = sa_parse_list_marker($lines[$nextIndex]);

            if ($nextMarker !== null && $nextMarker['type'] === $type) {
                $index++;
                continue;
            }

            break;
        }

        if (
            preg_match('/^#{1,6}\s+/', $trimmed)
            || sa_is_quiz_question_start($trimmed)
            || preg_match('/^```/', $trimmed)
            || preg_match('/^\$\$/', $trimmed)
            || sa_is_table_start($lines, $index)
        ) {
            break;
        }

        $marker = sa_parse_list_marker($line);

        if ($marker !== null) {
            if ($marker['type'] !== $type) {
                break;
            }

            if ($current !== null) {
                $items[] = trim($current);
            }

            $current = $marker['content'];
            $index++;
            continue;
        }

        if ($current === null) {
            break;
        }

        $current .= ' ' . $trimmed;
        $index++;
    }

    if ($current !== null) {
        $items[] = trim($current);
    }

    if (empty($items)) {
        return '';
    }

    $attrs = '';

    if ($type === 'ol' && $start !== null && $start !== 1) {
        $attrs = ' start="' . (int)$start . '"';
    }

    $html = '<' . $type . $attrs . '>';

    foreach ($items as $item) {
        $html .= '<li>' . sa_inline_markdown($item) . '</li>';
    }

    $html .= '</' . $type . '>';

    return $html;
}

function sa_render_math_block($formula) {
    $formula = trim((string)$formula);

    if ($formula === '') {
        return '';
    }

    return '<div class="math-block">\\[' . htmlspecialchars($formula, ENT_NOQUOTES, 'UTF-8') . '\\]</div>';
}

function sa_render_markdown($markdown) {
    $markdown = sa_strip_frontmatter($markdown);
    $lines = preg_split('/\n/', $markdown);

    $html = '';
    $paragraph = [];
    $inCode = false;
    $codeBuffer = [];
    $inMathBlock = false;
    $mathBuffer = [];

    $flushParagraph = function () use (&$html, &$paragraph) {
        if (!empty($paragraph)) {
            $html .= '<p>' . sa_inline_markdown(implode(' ', $paragraph)) . '</p>';
            $paragraph = [];
        }
    };

    for ($i = 0; $i < count($lines); $i++) {
        $line = $lines[$i];
        $trimmed = trim($line);

        if (preg_match('/^```/', $trimmed)) {
            $flushParagraph();

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

        if (preg_match('/^\$\$\s*(.*)$/', $trimmed, $matches)) {
            $flushParagraph();

            $afterOpening = trim($matches[1]);

            if ($afterOpening !== '' && substr($afterOpening, -2) === '$$') {
                $html .= sa_render_math_block(substr($afterOpening, 0, -2));
                continue;
            }

            $inMathBlock = true;
            $mathBuffer = [];

            if ($afterOpening !== '') {
                $mathBuffer[] = $afterOpening;
            }

            continue;
        }

        if ($inMathBlock) {
            if (preg_match('/^(.*?)\s*\$\$$/', $trimmed, $matches)) {
                $beforeClosing = trim($matches[1]);

                if ($beforeClosing !== '') {
                    $mathBuffer[] = $beforeClosing;
                }

                $html .= sa_render_math_block(implode("\n", $mathBuffer));
                $mathBuffer = [];
                $inMathBlock = false;
            } else {
                $mathBuffer[] = $line;
            }

            continue;
        }

        if ($trimmed === '') {
            $flushParagraph();
            continue;
        }

        if (sa_is_quiz_question_start($trimmed)) {
            $flushParagraph();
            $html .= sa_collect_quiz_question($lines, $i);
            $i--;
            continue;
        }

        if (sa_is_table_start($lines, $i)) {
            $flushParagraph();
            $html .= sa_collect_table($lines, $i);
            $i--;
            continue;
        }

        $listMarker = sa_parse_list_marker($line);

        if ($listMarker !== null) {
            $flushParagraph();
            $html .= sa_collect_list($lines, $i);
            $i--;
            continue;
        }

        if (preg_match('/^(#{1,6})\s+(.+)$/', $trimmed, $matches)) {
            $flushParagraph();

            $level = strlen($matches[1]);
            $text = trim($matches[2]);
            $slug = sa_slugify_heading($text);

            $html .= '<h' . $level . ' id="' . htmlspecialchars($slug, ENT_QUOTES, 'UTF-8') . '">' . sa_inline_markdown($text) . '</h' . $level . '>';
            continue;
        }

        $paragraph[] = $trimmed;
    }

    if ($inCode) {
        $html .= '<pre><code>' . htmlspecialchars(implode("\n", $codeBuffer), ENT_QUOTES, 'UTF-8') . '</code></pre>';
    }

    if ($inMathBlock) {
        $html .= sa_render_math_block(implode("\n", $mathBuffer));
    }

    $flushParagraph();

    return $html;
}

function add_heading_anchors(string $html): string {
    return preg_replace_callback('/(<h([2-4]) id="([^"]+)">)(.*?)(<\/h\2>)/i', function($matches) {
        $tagOpen = $matches[1];
        $id = $matches[3];
        $content = $matches[4];
        $tagClose = $matches[5];
        $anchorLink = ' <a href="#' . $id . '" class="heading-anchor" aria-hidden="true" title="Enlace directo">#</a>';
        
        return $tagOpen . $content . $anchorLink . $tagClose;
    }, $html);
}