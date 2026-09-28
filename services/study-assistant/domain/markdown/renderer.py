import re
import html
import unicodedata
from markdown_it import MarkdownIt

# Inicializar el parser de markdown con soporte para HTML y tablas
md = MarkdownIt('commonmark', {'html': True}).enable('table')


def strip_frontmatter(markdown: str) -> str:
    """
    Elimina el bloque de frontmatter YAML al inicio del documento.
    """
    return re.sub(r'^---\s*\n.*?\n---\s*\n', '', markdown, flags=re.DOTALL)


def _slugify_heading(text: str) -> str:
    """
    Convierte un texto de encabezado en un slug amigable para URLs.
    Maneja caracteres en español y elimina etiquetas HTML.
    """
    # Eliminar etiquetas HTML
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip().lower()
    # Normalizar acentos y caracteres especiales (ej. á -> a)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Reemplazar caracteres no alfanuméricos con guiones
    text = re.sub(r'[^\w]+', '-', text)
    # Eliminar guiones al inicio y al final
    return text.strip('-')


def add_heading_anchors(html_content: str) -> str:
    """
    Encuentra etiquetas <h2>, <h3>, <h4> en el HTML y:
    1. Genera un slug a partir del texto del encabezado.
    2. Añade un atributo id con el slug.
    3. Añade un ancla con la clase heading-anchor.
    """
    def repl(m):
        tag_name = m.group(1)
        content = m.group(2)
        slug = _slugify_heading(content)
        return f'<{tag_name} id="{slug}">{content}<a href="#{slug}" class="heading-anchor">#</a></{tag_name}>'
        
    return re.sub(r'<(h[234])[^>]*>(.*?)</\1>', repl, html_content, flags=re.IGNORECASE | re.DOTALL)


def _rewrite_images(html_content: str, note_id: str) -> str:
    """
    Reescribe las URLs de imágenes locales para que apunten al endpoint correcto.
    """
    def repl(m):
        prefix = m.group(1)
        src = m.group(2)
        suffix = m.group(3)
        
        # Ignorar URLs absolutas, data URIs y anclas
        if re.match(r'^(https?://|data:|#)', src, re.IGNORECASE):
            return m.group(0)
            
        # Ignorar si ya tiene el prefijo o es absoluta de la raíz
        if src.startswith(f'/assets/notes/{note_id}/') or src.startswith('/'):
            return m.group(0)
            
        new_src = f"/assets/notes/{note_id}/{src}"
        return f'{prefix}src="{new_src}"{suffix}'
        
    return re.sub(r'(<img[^>]+)src="([^"]+)"([^>]*>)', repl, html_content, flags=re.IGNORECASE)


def render_inline(text: str, note_id: str | None = None) -> str:
    """
    Renderiza una sola línea de Markdown (sin elementos de bloque).
    """
    html_output = md.renderInline(text)
    if note_id:
        html_output = _rewrite_images(html_output, note_id)
    return html_output


def render(markdown: str, note_id: str | None = None) -> str:
    """
    Función principal de renderizado. 
    Convierte Markdown a HTML con soporte para matemáticas, mermaid, quiz cards y notas.
    """
    # 1. Strip YAML frontmatter
    markdown = strip_frontmatter(markdown)
    
    placeholders = {}
    
    def save_placeholder(prefix: str, content: str) -> str:
        idx = len(placeholders)
        ph = f"%%SA_{prefix}_{idx}%%"
        placeholders[ph] = content
        return ph

    # 2. Proteger bloques matemáticos LaTeX ($$...$$)
    def repl_math_block(m):
        formula = html.escape(m.group(1).strip(), quote=False)
        return save_placeholder("MATH_BLOCK", f'<div class="math-block">\\[{formula}\\]</div>')
        
    markdown = re.sub(r'\$\$(.*?)\$\$', repl_math_block, markdown, flags=re.DOTALL)
    
    # 2. Proteger matemáticas inline ($...$)
    def repl_math_inline(m):
        formula = html.escape(m.group(1), quote=False)
        return save_placeholder("MATH_INLINE", f'<span class="math-inline">\\({formula}\\)</span>')
        
    markdown = re.sub(r'(?<!\\)\$([^$\n]+)(?<!\\)\$', repl_math_inline, markdown)
    
    # 3. Proteger bloques Mermaid
    def repl_mermaid(m):
        content = m.group(1).strip()
        escaped = html.escape(content, quote=True)
        cls = 'mermaid mermaid-mindmap' if content.lower().startswith('mindmap') else 'mermaid'
        return save_placeholder("MERMAID", f'<pre class="{cls}">{escaped}</pre>')
        
    markdown = re.sub(r'```mermaid\s*\n(.*?)```', repl_mermaid, markdown, flags=re.IGNORECASE | re.DOTALL)
    
    # 4. y 5. Detectar y extraer Quiz Cards y Callouts (Notas)
    lines = markdown.split('\n')
    out_lines = []
    i = 0
    n = len(lines)
    
    while i < n:
        line = lines[i]
        
        # 5. Detectar bloques Callout/Nota (> Nota: o > Note:)
        callout_match = re.match(r'^\s*>\s?(Nota|Note):\s*(.*)$', line, re.IGNORECASE)
        if callout_match:
            content_lines = [callout_match.group(2).strip()]
            i += 1
            while i < n:
                curr = lines[i]
                if re.match(r'^\s*>', curr):
                    curr_clean = re.sub(r'^\s*>\s?', '', curr).strip()
                    content_lines.append(curr_clean)
                    i += 1
                else:
                    break
            
            paragraphs = []
            cur_p = []
            for cl in content_lines:
                if not cl.strip():
                    if cur_p:
                        paragraphs.append(" ".join(cur_p))
                        cur_p = []
                else:
                    cur_p.append(cl)
            if cur_p:
                paragraphs.append(" ".join(cur_p))
                
            p_htmls = [f'<p>{render_inline(p, note_id)}</p>' for p in paragraphs]
            body_html = "".join(p_htmls)
            
            ph = save_placeholder("NOTE", f'<aside class="note"><div class="note-body">{body_html}</div></aside>')
            out_lines.append(ph)
            continue
            
        # 4. Detectar Quiz Cards
        quiz_match = re.match(r'^\s*(?:\*\*)?Pregunta\s+(\d+)\.(?:\*\*)?\s*(.*)$', line, re.IGNORECASE)
        if quiz_match:
            question_num = quiz_match.group(1)
            question_text = [quiz_match.group(2).strip()]
            options = []
            answer_text = ""
            i += 1
            
            while i < n:
                curr = lines[i].strip()
                if not curr:
                    i += 1
                    continue
                    
                # Si encontramos un nuevo encabezado o pregunta, terminamos
                if re.match(r'^#{1,6}\s+', curr) or re.match(r'^\s*(?:\*\*)?Pregunta\s+(\d+)\.', curr, re.IGNORECASE):
                    break
                    
                # Detectar respuesta correcta
                ans_match = re.match(r'^(?:\*\*)?Respuesta correcta:\s*(?:\*\*)?(.*)$', curr, re.IGNORECASE)
                if ans_match:
                    answer_text = ans_match.group(1).strip()
                    i += 1
                    while i < n:
                        next_curr = lines[i].strip()
                        if not next_curr:
                            break
                        if re.match(r'^#{1,6}\s+', next_curr) or re.match(r'^\s*(?:\*\*)?Pregunta\s+(\d+)\.', next_curr, re.IGNORECASE):
                            break
                        answer_text += " " + next_curr
                        i += 1
                    break
                    
                # Detectar opciones A) B) etc.
                opt_match = re.match(r'^([A-D])[\.)]\s+(.+)$', curr, re.IGNORECASE)
                if opt_match:
                    options.append(opt_match.group(2).strip())
                else:
                    if options:
                        options[-1] += " " + curr
                    else:
                        question_text.append(curr)
                i += 1
                
            q_html = render_inline(" ".join(question_text), note_id)
            html_parts = [
                f'<div class="quiz-card">',
                f'  <div class="quiz-question"><strong>Pregunta {question_num}.</strong> {q_html}</div>'
            ]
            if options:
                html_parts.append('  <ol type="A" class="quiz-options">')
                for opt in options:
                    opt_html = render_inline(opt, note_id)
                    html_parts.append(f'    <li>{opt_html}</li>')
                html_parts.append('  </ol>')
                
            if answer_text:
                ans_html = render_inline(answer_text, note_id)
                html_parts.append('  <details class="quiz-answer">')
                html_parts.append('    <summary>Mostrar respuesta y explicaci&oacute;n</summary>')
                html_parts.append(f'    <div class="quiz-answer-content"><strong>Respuesta correcta:</strong> {ans_html}</div>')
                html_parts.append('  </details>')
            html_parts.append('</div>')
            
            ph = save_placeholder("QUIZ", "\n".join(html_parts))
            out_lines.append(ph)
            continue
            
        out_lines.append(line)
        i += 1
        
    processed_markdown = "\n".join(out_lines)
    
    # 6. Parsear el resto del Markdown
    html_output = md.render(processed_markdown)
    
    # 7. Restaurar todos los placeholders
    # Invertimos el orden para garantizar que los placeholders anidados (ej. MATH dentro de QUIZ) se restauren correctamente
    for ph in reversed(list(placeholders.keys())):
        html_output = html_output.replace(ph, placeholders[ph])
        
    # 8. Reescribir URLs de imágenes
    if note_id:
        html_output = _rewrite_images(html_output, note_id)
        
    # 9. Añadir anclas a los encabezados
    html_output = add_heading_anchors(html_output)
    
    return html_output
