<?php

declare(strict_types=1);

require_once __DIR__ . '/autoload.php';

use StudyAssistant\Markdown\MarkdownRenderer;

/**
 * Facade procedural de renderizado Markdown para compatibilidad hacia atrás.
 * Delega en StudyAssistant\Markdown\MarkdownRenderer.
 */

function sa_normalize_markdown(mixed $markdown): string
{
    return (new MarkdownRenderer())->normalize((string)$markdown);
}

function sa_strip_frontmatter(mixed $markdown): string
{
    return (new MarkdownRenderer())->stripFrontmatter((string)$markdown);
}

function sa_math_placeholder(int|string $key): string
{
    return '%%SA_MATH_' . $key . '%%';
}

function sa_extract_inline_math(string $text, array &$mathBlocks): string
{
    return preg_replace_callback('/(?<!\\\\)\$([^$\n]+)(?<!\\\\)\$/', function ($matches) use (&$mathBlocks) {
        $key = count($mathBlocks);
        $mathBlocks[$key] = [
            'type' => 'inline',
            'content' => $matches[1],
        ];

        return sa_math_placeholder($key);
    }, $text) ?? $text;
}

function sa_restore_math_placeholders(string $html, array $mathBlocks): string
{
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

function sa_render_context(?string $noteId = null, bool $set = false): ?string
{
    static $currentNoteId = null;

    if ($set) {
        $currentNoteId = $noteId;
    }

    return $currentNoteId;
}

function sa_render_details_block(string $detailsHtml): string
{
    $detailsHtml = trim($detailsHtml);
    $detailsHtml = preg_replace('/^\s*<details\b[^>]*>\s*/is', '', $detailsHtml) ?? $detailsHtml;
    $detailsHtml = preg_replace('/\s*<\/details>\s*$/is', '', $detailsHtml) ?? $detailsHtml;

    if (preg_match('/^(.*?)(<summary\b[^>]*>.*?<\/summary>\s*)(.*)$/is', $detailsHtml, $matches)) {
        $summaryHtml = $matches[2];
        $body = trim($matches[3]);
        $bodyHtml = $body === '' ? '' : sa_render_markdown($body, sa_render_context());

        return '<details>' . $summaryHtml . $bodyHtml . '</details>';
    }

    return '<details>' . sa_render_markdown($detailsHtml, sa_render_context()) . '</details>';
}

function sa_inline_markdown(mixed $text): string
{
    return (new MarkdownRenderer(sa_render_context()))->renderInline((string)$text);
}

function sa_slugify_heading(mixed $text): string
{
    return (new MarkdownRenderer())->slugify((string)$text);
}

function sa_render_table(array $lines): string
{
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
            $cell = str_replace("\n", '%%SA_BR%%', $cell);
            $cell = str_ireplace(['<br>', '<br/>', '<br />'], '%%SA_BR%%', $cell);
            $cellHtml = sa_inline_markdown($cell);
            $cellHtml = str_replace('%%SA_BR%%', '<br>', $cellHtml);
            $html .= '<' . $tag . '>' . $cellHtml . '</' . $tag . '>';
        }

        $html .= '</tr>';
        $headerRendered = true;
    }

    $html .= '</table></div>';

    return $html;
}

function sa_has_pipe(mixed $line): bool
{
    return strpos(trim((string)$line), '|') !== false;
}

function sa_is_table_separator(mixed $line): bool
{
    return (bool)preg_match('/^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/', (string)$line);
}

function sa_is_table_start(array $lines, int $index): bool
{
    if (!isset($lines[$index + 1])) {
        return false;
    }

    return sa_has_pipe($lines[$index]) && sa_is_table_separator($lines[$index + 1]);
}

function sa_collect_table(array $lines, int &$index): string
{
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

function sa_is_quiz_question_start(mixed $line): bool
{
    return (bool)preg_match('/^\s*(?:\*\*)?Pregunta\s+([0-9]+)\.(?:\*\*)?\s*(.*)$/u', trim((string)$line));
}

function sa_parse_answer_line(mixed $line): ?string
{
    $clean = trim((string)$line);
    $clean = preg_replace('/^\*\*/', '', $clean) ?? $clean;
    $clean = preg_replace('/\*\*/', '', $clean) ?? $clean;

    if (!preg_match('/^Respuesta correcta:\s*(.+)$/u', $clean, $matches)) {
        return null;
    }

    return trim($matches[1]);
}

function sa_render_quiz_question(int|string $questionNumber, string $questionText, array $options, string $answerText): string
{
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

function sa_collect_quiz_question(array $lines, int &$index): string
{
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

        if (preg_match('/^([A-D])[\.)]\s+(.+)$/iu', $currentLine, $optionMatches)) {
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

function sa_parse_list_marker(mixed $line): ?array
{
    $line = (string)$line;
    if (preg_match('/^(\s*)([0-9]+)\.\s+(.+)$/u', $line, $matches)) {
        return [
            'type' => 'ol',
            'number' => (int)$matches[2],
            'content' => trim($matches[3]),
            'indent_spaces' => strlen($matches[1]),
        ];
    }

    if (preg_match('/^(\s*)([A-Za-z])[\.)]\s+(.+)$/u', $line, $matches)) {
        return [
            'type' => 'ol',
            'number' => null,
            'content' => trim($matches[3]),
            'indent_spaces' => strlen($matches[1]),
            'letter' => strtoupper($matches[2]),
        ];
    }

    if (preg_match('/^(\s*)[-*]\s+(.+)$/u', $line, $matches)) {
        return [
            'type' => 'ul',
            'number' => null,
            'content' => trim($matches[2]),
            'indent_spaces' => strlen($matches[1]),
        ];
    }

    return null;
}

function sa_next_non_empty_index(array $lines, int $index): ?int
{
    for ($i = $index; $i < count($lines); $i++) {
        if (trim($lines[$i]) !== '') {
            return $i;
        }
    }

    return null;
}

function sa_collect_list(array $lines, int &$index, int $parentIndent = 0): string
{
    $firstMarker = sa_parse_list_marker($lines[$index]);

    if ($firstMarker === null) {
        return '';
    }

    $type = $firstMarker['type'];
    $start = $firstMarker['number'];
    $baseIndent = $firstMarker['indent_spaces'] ?? 0;
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

            $nextLine = $lines[$nextIndex];
            $nextMarker = sa_parse_list_marker($nextLine);

            if ($nextMarker !== null && $nextMarker['type'] === $type && (($nextMarker['indent_spaces'] ?? 0) <= $baseIndent)) {
                $index = $nextIndex;
                break;
            }

            $trimNext = trim($nextLine);

            if (preg_match('/^#{1,6}\s+/', $trimNext)
                || sa_is_quiz_question_start($trimNext)
                || preg_match('/^```/', $trimNext)
                || preg_match('/^\$\$/', $trimNext)
                || sa_is_table_start($lines, $nextIndex)) {
                $index = $nextIndex;
                break;
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
            $markerIndent = $marker['indent_spaces'] ?? 0;

            if ($markerIndent < $baseIndent) {
                break;
            }

            if ($markerIndent > $baseIndent) {
                $nestedHtml = sa_collect_list($lines, $index, $baseIndent);

                if ($current !== null) {
                    $current['nested'] .= $nestedHtml;
                }

                continue;
            }

            if ($marker['type'] !== $type) {
                break;
            }

            if ($current !== null) {
                $items[] = $current;
            }

            $current = ['text' => $marker['content'], 'nested' => ''];
            $index++;
            continue;
        }

        if ($current === null) {
            break;
        }

        $current['text'] .= ' ' . $trimmed;
        $index++;
    }

    if ($current !== null) {
        $items[] = $current;
    }

    if (empty($items)) {
        return '';
    }

    $attrs = '';

    if ($type === 'ol' && isset($firstMarker['letter'])) {
        $attrs = ' type="' . strtolower((string)$firstMarker['letter']) . '"';
    } elseif ($type === 'ol' && $start !== null && $start !== 1) {
        $attrs = ' start="' . (int)$start . '"';
    }

    $html = '<' . $type . $attrs . '>';

    foreach ($items as $item) {
        $html .= '<li>' . sa_inline_markdown($item['text']) . $item['nested'] . '</li>';
    }

    $html .= '</' . $type . '>';

    return $html;
}

function sa_render_math_block(mixed $formula): string
{
    $formula = trim((string)$formula);

    if ($formula === '') {
        return '';
    }

    return '<div class="math-block">\\[' . htmlspecialchars($formula, ENT_NOQUOTES, 'UTF-8') . '\\]</div>';
}

function sa_render_markdown(mixed $markdown, ?string $noteId = null): string
{
    return (new MarkdownRenderer())->render((string)$markdown, $noteId);
}

function add_heading_anchors(string $html): string
{
    return (new MarkdownRenderer())->addHeadingAnchors($html);
}