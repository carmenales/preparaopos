<?php

declare(strict_types=1);

namespace StudyAssistant\Markdown;

/**
 * Motor de renderizado Markdown a HTML nativo y de alto rendimiento.
 * Soporta extensiones de StudyAssistant:
 * - Fórmulas matemáticas LaTeX ($...$ inline y $$...$$ bloque) para MathJax.
 * - Bloques de diagramas Mermaid.js.
 * - Tarjetas interactivas de preguntas tipo test (quiz-cards).
 * - Tablas GFM con saltos de línea internos.
 * - Bloques de notas y callouts (<aside class="note">).
 * - Reescritura segura de imágenes relativas vía asset.php.
 * - Anclas accesibles en encabezados h2-h4.
 */
class MarkdownRenderer
{
    private ?string $currentNoteId = null;

    public function __construct(?string $noteId = null)
    {
        $this->currentNoteId = $noteId;
    }

    /**
     * Renderiza un documento Markdown completo a HTML seguro.
     */
    public function render(string $markdown, ?string $noteId = null): string
    {
        $this->currentNoteId = $noteId ?? $this->currentNoteId;

        $markdown = $this->stripFrontmatter($markdown);
        $lines = preg_split('/\n/', $markdown) ?: [];

        $html = '';
        $paragraph = [];
        $inCode = false;
        $codeBuffer = [];
        $inMermaid = false;
        $mermaidBuffer = [];
        $mermaidClass = '';
        $inDetails = false;
        $detailsBuffer = [];
        $inMathBlock = false;
        $mathBuffer = [];

        $flushParagraph = function () use (&$html, &$paragraph): void {
            if (!empty($paragraph)) {
                $html .= '<p>' . $this->renderInline(implode(' ', $paragraph)) . '</p>';
                $paragraph = [];
            }
        };

        $totalLines = count($lines);
        for ($i = 0; $i < $totalLines; $i++) {
            $line = $lines[$i];
            $trimmed = trim($line);

            // Bloques <details> nativos
            if ($inDetails) {
                $detailsBuffer[] = $line;
                if (stripos($line, '</details>') !== false) {
                    $html .= $this->renderDetailsBlock(implode("\n", $detailsBuffer));
                    $detailsBuffer = [];
                    $inDetails = false;
                }
                continue;
            }

            if (preg_match('/^<details\b/i', $trimmed)) {
                $flushParagraph();
                $inDetails = true;
                $detailsBuffer = [$line];
                if (stripos($trimmed, '</details>') !== false) {
                    $html .= $this->renderDetailsBlock(implode("\n", $detailsBuffer));
                    $detailsBuffer = [];
                    $inDetails = false;
                }
                continue;
            }

            // Bloques Mermaid
            if (preg_match('/^```mermaid\s*$/i', $trimmed)) {
                $flushParagraph();
                if ($inMermaid) {
                    $html .= '<pre class="mermaid' . $mermaidClass . '">' . htmlspecialchars(implode("\n", $mermaidBuffer), ENT_QUOTES, 'UTF-8') . '</pre>';
                    $mermaidBuffer = [];
                    $mermaidClass = '';
                    $inMermaid = false;
                    continue;
                }

                $inMermaid = true;
                $mermaidBuffer = [];
                $mermaidClass = '';
                continue;
            }

            if ($inMermaid) {
                if (preg_match('/^```\s*$/', $trimmed)) {
                    $html .= '<pre class="mermaid' . $mermaidClass . '">' . htmlspecialchars(implode("\n", $mermaidBuffer), ENT_QUOTES, 'UTF-8') . '</pre>';
                    $mermaidBuffer = [];
                    $mermaidClass = '';
                    $inMermaid = false;
                    continue;
                }

                if ($mermaidClass === '' && preg_match('/^\s*(mindmap|graph|flowchart|sequenceDiagram|classDiagram|erDiagram|journey|pie|gantt|stateDiagram|xychart)\b/i', $line, $mmMatch)) {
                    if (strtolower($mmMatch[1]) === 'mindmap') {
                        $mermaidClass = ' mermaid-mindmap';
                    }
                }

                $mermaidBuffer[] = $line;
                continue;
            }

            // Bloques de código genéricos
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

            if ($inMathBlock) {
                if (preg_match('/^(.*?)\s*\$\$$/', $trimmed, $matches)) {
                    $beforeClosing = trim($matches[1]);
                    if ($beforeClosing !== '') {
                        $mathBuffer[] = $beforeClosing;
                    }
                    $html .= $this->renderMathBlock(implode("\n", $mathBuffer));
                    $mathBuffer = [];
                    $inMathBlock = false;
                } else {
                    $mathBuffer[] = $line;
                }
                continue;
            }

            // Bloques de matemáticas en bloque ($$...$$)
            if (preg_match('/^\$\$\s*(.*)$/', $trimmed, $matches)) {
                $flushParagraph();
                $afterOpening = trim($matches[1]);
                if ($afterOpening !== '' && substr($afterOpening, -2) === '$$') {
                    $html .= $this->renderMathBlock(substr($afterOpening, 0, -2));
                    continue;
                }

                $inMathBlock = true;
                $mathBuffer = [];
                if ($afterOpening !== '') {
                    $mathBuffer[] = $afterOpening;
                }
                continue;
            }

            // Líneas vacías
            if ($trimmed === '') {
                $flushParagraph();
                continue;
            }

            // Saltos <br>
            if (preg_match('/^<br\s*\/?>$/i', $trimmed)) {
                $flushParagraph();
                $html .= '<br>';
                continue;
            }

            // Reglas horizontales <hr>
            if (preg_match('/^<hr\s*\/?>$/i', $trimmed) || preg_match('/^(?:-{3,}|\*{3,}|_{3,})$/', $trimmed)) {
                $flushParagraph();
                $html .= '<hr>';
                continue;
            }

            // Párrafo explícito <p>
            if (preg_match('/^<p\b/i', $trimmed)) {
                $flushParagraph();
                $html .= $this->renderInline($trimmed);
                continue;
            }

            // Preguntas de test interactivas (quiz cards)
            if ($this->isQuizQuestionStart($trimmed)) {
                $flushParagraph();
                $html .= $this->collectQuizQuestion($lines, $i);
                $i--;
                continue;
            }

            // Tablas Markdown (GFM)
            if ($this->isTableStart($lines, $i)) {
                $flushParagraph();
                $html .= $this->collectTable($lines, $i);
                $i--;
                continue;
            }

            // Listas ordenadas y no ordenadas
            $listMarker = $this->parseListMarker($line);
            if ($listMarker !== null) {
                $flushParagraph();
                $html .= $this->collectList($lines, $i, 0);
                $i--;
                continue;
            }

            // Encabezados (# Título)
            if (preg_match('/^(#{1,6})\s+(.+)$/', $trimmed, $matches)) {
                $flushParagraph();
                $level = strlen($matches[1]);
                $text = trim($matches[2]);
                $slug = $this->slugifyHeading($text);
                $html .= '<h' . $level . ' id="' . htmlspecialchars($slug, ENT_QUOTES, 'UTF-8') . '">' . $this->renderInline($text) . '</h' . $level . '>';
                continue;
            }

            // Citas / Callouts (> Nota:)
            if (preg_match('/^>/', $trimmed)) {
                $flushParagraph();
                $bq = [];
                while ($i < $totalLines && preg_match('/^\s*>\s?(.*)$/', $lines[$i], $m)) {
                    $bq[] = $m[1];
                    $i++;
                }
                if (!empty($bq)) {
                    $i--;
                }

                if (!empty($bq) && preg_match('/^(Nota|Note):/iu', $bq[0])) {
                    $bq[0] = preg_replace('/^(Nota|Note):/iu', '', $bq[0]);
                }

                $paragraphs = [];
                $currentParagraph = '';
                foreach ($bq as $bqLine) {
                    if (trim($bqLine) === '') {
                        if ($currentParagraph !== '') {
                            $paragraphs[] = $currentParagraph;
                            $currentParagraph = '';
                        }
                        continue;
                    }
                    if ($currentParagraph !== '') {
                        $currentParagraph .= ' ' . $bqLine;
                    } else {
                        $currentParagraph = $bqLine;
                    }
                }
                if ($currentParagraph !== '') {
                    $paragraphs[] = $currentParagraph;
                }

                $noteHtml = '';
                foreach ($paragraphs as $noteParagraph) {
                    $noteHtml .= '<p>' . $this->renderInline(trim($noteParagraph)) . '</p>';
                }
                $html .= '<aside class="note"><div class="note-body">' . $noteHtml . '</div></aside>';
                continue;
            }

            $paragraph[] = $trimmed;
        }

        if ($inCode) {
            $html .= '<pre><code>' . htmlspecialchars(implode("\n", $codeBuffer), ENT_QUOTES, 'UTF-8') . '</code></pre>';
        }
        if ($inMermaid) {
            $html .= '<pre class="mermaid">' . htmlspecialchars(implode("\n", $mermaidBuffer), ENT_QUOTES, 'UTF-8') . '</pre>';
        }
        if ($inMathBlock) {
            $html .= $this->renderMathBlock(implode("\n", $mathBuffer));
        }

        $flushParagraph();
        return $html;
    }

    /**
     * Normaliza saltos de línea y tabulaciones en el Markdown.
     */
    public function normalize(string $markdown): string
    {
        $markdown = preg_replace('/^\xEF\xBB\xBF/', '', $markdown) ?? $markdown;
        $markdown = str_replace(["\r\n", "\r"], "\n", $markdown);

        $markdown = preg_replace_callback('/^([ \t]+)/m', static function (array $m): string {
            return str_replace("\t", "    ", $m[1]);
        }, $markdown) ?? $markdown;

        return $markdown;
    }

    /**
     * Elimina el bloque frontmatter YAML inicial si existe.
     */
    public function stripFrontmatter(string $markdown): string
    {
        $markdown = $this->normalize($markdown);
        if (preg_match('/\A---\s*\n.*?\n---\s*\n/s', $markdown, $matches)) {
            return substr($markdown, strlen($matches[0]));
        }
        return $markdown;
    }

    /**
     * Renderiza formato inline (negrita, cursiva, enlaces, imágenes, fórmulas, código inline).
     */
    public function renderInline(string $text, ?string $noteId = null): string
    {
        $noteId = $noteId ?? $this->currentNoteId;
        $mathBlocks = [];
        $text = $this->extractInlineMath($text, $mathBlocks);

        $codeSpans = [];
        $text = preg_replace_callback('/`([^`]+)`/', function (array $m) use (&$codeSpans): string {
            $placeholder = '%%SA_CODE_' . count($codeSpans) . '%%';
            $codeSpans[$placeholder] = '<code>' . htmlspecialchars($m[1], ENT_QUOTES, 'UTF-8') . '</code>';
            return $placeholder;
        }, $text) ?? $text;

        $htmlTags = [];
        $safeTagRegex = '#</?(?:br|sup|sub|b|i|u|strong|em|mark|small|del|s|strike|abbr|p|span)(?:\s+[a-zA-Z0-9_\-]+(?:=(?:"[^"]*"|\'[^\']*\'))?)*\s*/?>|<a(?:\s+[a-zA-Z0-9_\-]+(?:=(?:"[^"]*"|\'[^\']*\'))?)*\s*>|</a>#i';

        $text = preg_replace_callback($safeTagRegex, function (array $m) use (&$htmlTags): string {
            $placeholder = '%%SA_HTML_' . count($htmlTags) . '%%';
            $htmlTags[$placeholder] = $m[0];
            return $placeholder;
        }, $text) ?? $text;

        $html = htmlspecialchars($text, ENT_QUOTES, 'UTF-8');

        if (!empty($htmlTags)) {
            $html = strtr($html, $htmlTags);
        }

        $html = preg_replace('/\*\*([^*]+)\*\*/', '<strong>$1</strong>', $html) ?? $html;
        $html = preg_replace('/\*([^*]+)\*/', '<em>$1</em>', $html) ?? $html;

        // Imágenes con resolución de asset.php para rutas relativas locales
        $html = preg_replace_callback('/!\[([^\]]*)\]\(([^)]+)\)/', function (array $matches) use ($noteId): string {
            $alt = $matches[1];
            $path = $matches[2];

            if ($noteId !== null && !preg_match('#^https?://#i', $path)) {
                $src = 'asset.php?note=' . urlencode($noteId) . '&path=' . urlencode($path);
            } else {
                $src = $path;
            }

            return '<img src="' . htmlspecialchars($src, ENT_QUOTES, 'UTF-8') . '" alt="' . htmlspecialchars($alt, ENT_QUOTES, 'UTF-8') . '" loading="lazy">';
        }, $html) ?? $html;

        // Enlaces
        $html = preg_replace_callback('/\[([^\]]+)\]\(([^)]+)\)/', function (array $matches): string {
            $linkText = $matches[1];
            $path = $matches[2];
            $escapedPath = htmlspecialchars($path, ENT_QUOTES, 'UTF-8');

            if (preg_match('/^\s*#/u', $path)) {
                return '<a href="' . $escapedPath . '">' . $linkText . '</a>';
            }

            if (preg_match('#^https?://#i', $path)) {
                return '<a href="' . $escapedPath . '" target="_blank" rel="noopener noreferrer">' . $linkText . '</a>';
            }

            return '<a href="' . $escapedPath . '">' . $linkText . '</a>';
        }, $html) ?? $html;

        if (!empty($codeSpans)) {
            $html = strtr($html, $codeSpans);
        }

        return $this->restoreMathPlaceholders($html, $mathBlocks);
    }

    public function extractInlineMath(string $text, array &$mathBlocks): string
    {
        return preg_replace_callback('/(?<!\\\\)\$([^$\n]+)(?<!\\\\)\$/', function (array $matches) use (&$mathBlocks): string {
            $key = count($mathBlocks);
            $mathBlocks[$key] = [
                'type' => 'inline',
                'content' => $matches[1],
            ];
            return '%%SA_MATH_' . $key . '%%';
        }, $text) ?? $text;
    }

    public function restoreMathPlaceholders(string $html, array $mathBlocks): string
    {
        foreach ($mathBlocks as $key => $math) {
            $placeholder = '%%SA_MATH_' . $key . '%%';
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

    public function renderMathBlock(string $formula): string
    {
        $formula = trim($formula);
        if ($formula === '') {
            return '';
        }
        return '<div class="math-block">\\[' . htmlspecialchars($formula, ENT_NOQUOTES, 'UTF-8') . '\\]</div>';
    }

    public function renderDetailsBlock(string $detailsHtml): string
    {
        $detailsHtml = trim($detailsHtml);
        $detailsHtml = preg_replace('/^\s*<details\b[^>]*>\s*/is', '', $detailsHtml) ?? $detailsHtml;
        $detailsHtml = preg_replace('/\s*<\/details>\s*$/is', '', $detailsHtml) ?? $detailsHtml;

        if (preg_match('/^(.*?)(<summary\b[^>]*>.*?<\/summary>\s*)(.*)$/is', $detailsHtml, $matches)) {
            $summaryHtml = $matches[2];
            $body = trim($matches[3]);
            $bodyHtml = $body === '' ? '' : $this->render($body);
            return '<details>' . $summaryHtml . $bodyHtml . '</details>';
        }

        return '<details>' . $this->render($detailsHtml) . '</details>';
    }

    public function renderTable(array $lines): string
    {
        $html = '<div class="table-wrapper"><table>';
        $headerRendered = false;

        foreach ($lines as $index => $line) {
            if ($index === 1 && $this->isTableSeparator($line)) {
                continue;
            }

            $cells = array_map('trim', explode('|', trim($line, '| ')));
            $tag = $headerRendered ? 'td' : 'th';
            $html .= '<tr>';

            foreach ($cells as $cell) {
                $cell = str_replace("\n", '%%SA_BR%%', $cell);
                $cell = str_ireplace(['<br>', '<br/>', '<br />'], '%%SA_BR%%', $cell);
                $cellHtml = $this->renderInline($cell);
                $cellHtml = str_replace('%%SA_BR%%', '<br>', $cellHtml);
                $html .= '<' . $tag . '>' . $cellHtml . '</' . $tag . '>';
            }

            $html .= '</tr>';
            $headerRendered = true;
        }

        $html .= '</table></div>';
        return $html;
    }

    public function hasPipe(string $line): bool
    {
        return strpos(trim($line), '|') !== false;
    }

    public function isTableSeparator(string $line): bool
    {
        return (bool)preg_match('/^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/', $line);
    }

    public function isTableStart(array $lines, int $index): bool
    {
        if (!isset($lines[$index + 1])) {
            return false;
        }
        return $this->hasPipe($lines[$index]) && $this->isTableSeparator($lines[$index + 1]);
    }

    public function collectTable(array $lines, int &$index): string
    {
        $tableLines = [];
        $total = count($lines);

        while ($index < $total) {
            $line = $lines[$index];
            if (trim($line) === '') {
                break;
            }
            if (!$this->hasPipe($line) && !$this->isTableSeparator($line)) {
                break;
            }
            $tableLines[] = $line;
            $index++;
        }

        return $this->renderTable($tableLines);
    }

    public function isQuizQuestionStart(string $line): bool
    {
        return (bool)preg_match('/^\s*(?:\*\*)?Pregunta\s+([0-9]+)\.(?:\*\*)?\s*(.*)$/u', trim($line));
    }

    public function parseAnswerLine(string $line): ?string
    {
        $clean = trim($line);
        $clean = preg_replace('/^\*\*/', '', $clean) ?? $clean;
        $clean = preg_replace('/\*\*/', '', $clean) ?? $clean;

        if (!preg_match('/^Respuesta correcta:\s*(.+)$/u', $clean, $matches)) {
            return null;
        }
        return trim($matches[1]);
    }

    public function renderQuizQuestion(int $questionNumber, string $questionText, array $options, string $answerText): string
    {
        $html = '<section class="quiz-card">';
        $html .= '<div class="quiz-question-label">Pregunta ' . $questionNumber . '</div>';
        $html .= '<div class="quiz-question-text">' . $this->renderInline($questionText) . '</div>';

        if (!empty($options)) {
            $html .= '<ol class="quiz-options" type="A">';
            foreach ($options as $option) {
                $html .= '<li>' . $this->renderInline($option) . '</li>';
            }
            $html .= '</ol>';
        }

        if ($answerText !== '') {
            $html .= '<details class="quiz-answer">';
            $html .= '<summary>Mostrar respuesta y explicación</summary>';
            $html .= '<div>' . $this->renderInline($answerText) . '</div>';
            $html .= '</details>';
        }

        $html .= '</section>';
        return $html;
    }

    public function collectQuizQuestion(array $lines, int &$index): string
    {
        $line = trim($lines[$index]);
        preg_match('/^\s*(?:\*\*)?Pregunta\s+([0-9]+)\.(?:\*\*)?\s*(.*)$/u', $line, $matches);

        $questionNumber = (int)$matches[1];
        $questionParts = [];
        $initialText = trim($matches[2] ?? '');

        if ($initialText !== '') {
            $questionParts[] = $initialText;
        }

        $options = [];
        $answerText = '';
        $currentOptionIndex = null;
        $index++;
        $total = count($lines);

        while ($index < $total) {
            $currentLine = trim($lines[$index]);
            if ($currentLine === '') {
                $index++;
                continue;
            }

            if (preg_match('/^#{1,6}\s+/', $currentLine) || $this->isQuizQuestionStart($currentLine)) {
                break;
            }

            $parsedAnswer = $this->parseAnswerLine($currentLine);
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

        return $this->renderQuizQuestion(
            $questionNumber,
            trim(implode(' ', $questionParts)),
            $options,
            $answerText
        );
    }

    public function parseListMarker(string $line): ?array
    {
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

    public function collectList(array $lines, int &$index, int $parentIndent = 0): string
    {
        $firstMarker = $this->parseListMarker($lines[$index]);
        if ($firstMarker === null) {
            return '';
        }

        $type = $firstMarker['type'];
        $start = $firstMarker['number'];
        $baseIndent = $firstMarker['indent_spaces'] ?? 0;
        $items = [];
        $current = null;
        $total = count($lines);

        while ($index < $total) {
            $line = $lines[$index];
            $trimmed = trim($line);

            if ($trimmed === '') {
                $nextIndex = null;
                for ($k = $index + 1; $k < $total; $k++) {
                    if (trim($lines[$k]) !== '') {
                        $nextIndex = $k;
                        break;
                    }
                }

                if ($nextIndex === null) {
                    $index++;
                    break;
                }

                $nextLine = $lines[$nextIndex];
                $nextMarker = $this->parseListMarker($nextLine);

                if ($nextMarker !== null && $nextMarker['type'] === $type && (($nextMarker['indent_spaces'] ?? 0) <= $baseIndent)) {
                    $index = $nextIndex;
                    break;
                }

                $trimNext = trim($nextLine);
                if (preg_match('/^#{1,6}\s+/', $trimNext)
                    || $this->isQuizQuestionStart($trimNext)
                    || preg_match('/^```/', $trimNext)
                    || preg_match('/^\$\$/', $trimNext)
                    || $this->isTableStart($lines, $nextIndex)) {
                    $index = $nextIndex;
                    break;
                }

                break;
            }

            if (
                preg_match('/^#{1,6}\s+/', $trimmed)
                || $this->isQuizQuestionStart($trimmed)
                || preg_match('/^```/', $trimmed)
                || preg_match('/^\$\$/', $trimmed)
                || $this->isTableStart($lines, $index)
            ) {
                break;
            }

            $marker = $this->parseListMarker($line);

            if ($marker !== null) {
                $markerIndent = $marker['indent_spaces'] ?? 0;

                if ($markerIndent < $baseIndent) {
                    break;
                }

                if ($markerIndent > $baseIndent) {
                    $nestedHtml = $this->collectList($lines, $index, $baseIndent);
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
            $attrs = ' start="' . $start . '"';
        }

        $html = '<' . $type . $attrs . '>';
        foreach ($items as $item) {
            $html .= '<li>' . $this->renderInline($item['text']) . $item['nested'] . '</li>';
        }
        $html .= '</' . $type . '>';

        return $html;
    }

    public function slugifyHeading(string $text): string
    {
        $text = trim($text);
        $text = iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $text) ?: $text;
        $text = preg_replace('/[^\p{L}\p{N}]+/u', '-', $text) ?? $text;
        $text = trim($text, '-');

        return function_exists('mb_strtolower') ? mb_strtolower($text, 'UTF-8') : strtolower($text);
    }

    public function slugify(string $text): string
    {
        return $this->slugifyHeading($text);
    }

    /**
     * Inyecta anclas directas accesibles (#slug) en los encabezados h2, h3 y h4.
     */
    public function addHeadingAnchors(string $html): string
    {
        return preg_replace_callback('/(<h([2-4]) id="([^"]+)">)(.*?)(<\/h\2>)/i', static function (array $matches): string {
            $tagOpen = $matches[1];
            $id = $matches[3];
            $content = $matches[4];
            $tagClose = $matches[5];
            $anchorLink = ' <a href="#' . $id . '" class="heading-anchor" aria-hidden="true" title="Enlace directo">#</a>';
            return $tagOpen . $content . $anchorLink . $tagClose;
        }, $html) ?? $html;
    }
}
