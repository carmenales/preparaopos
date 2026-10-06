"""Rutas del visor de apuntes individuales."""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from domain.markdown.renderer import render, add_heading_anchors
from infrastructure.knowledge_fs.repository import KnowledgeFSRepository

router = APIRouter()


def _build_toc_html(headings: list[dict]) -> str:
    """Construye el HTML del TOC jerárquico a partir de la lista de encabezados.

    Genera un árbol con <details>/<summary> colapsables para los nodos
    con hijos, replicando la estructura del TableOfContents.php original.
    """
    if not headings:
        return ""

    # Filtrar solo niveles 2, 3, 4
    filtered = [h for h in headings if 2 <= h.get("level", 0) <= 4]
    if not filtered:
        return ""

    # Construir árbol jerárquico
    tree: list[dict] = []
    stack: list[dict] = []

    for heading in filtered:
        node = {
            "text": heading.get("text", ""),
            "anchor": heading.get("anchor", ""),
            "level": heading.get("level", 2),
            "children": [],
        }

        # Buscar el padre correcto en la pila
        while stack and stack[-1]["level"] >= node["level"]:
            stack.pop()

        if stack:
            stack[-1]["children"].append(node)
        else:
            tree.append(node)

        stack.append(node)

    return _render_toc_tree(tree)


def _render_toc_tree(nodes: list[dict]) -> str:
    """Renderiza el árbol TOC a HTML con acordeones colapsables."""
    if not nodes:
        return ""

    html_parts = ['<ul class="nested-toc-list">']
    for node in nodes:
        anchor = node["anchor"]
        text = node["text"]

        if node["children"]:
            html_parts.append("<li>")
            html_parts.append(
                f'<details open class="toc-details">'
                f'<summary><a href="#{anchor}">{text}</a></summary>'
            )
            html_parts.append(_render_toc_tree(node["children"]))
            html_parts.append("</details>")
            html_parts.append("</li>")
        else:
            html_parts.append(
                f'<li><div class="toc-link-wrapper">'
                f'<a href="#{anchor}">{text}</a>'
                f"</div></li>"
            )

    html_parts.append("</ul>")
    return "\n".join(html_parts)


@router.get("/notes/{note_id}", response_class=HTMLResponse)
async def view_note(request: Request, note_id: str, process: str = ""):
    """Visor de apunte individual con TOC, renderizado Markdown y paginación."""
    from domain.notes.service import NoteService

    note_service: NoteService = request.app.state.note_service
    repo: KnowledgeFSRepository = request.app.state.repository
    templates = request.app.state.templates

    # Buscar la nota
    note = note_service.find_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Nota no encontrada: {note_id}")

    # Leer contenido Markdown del disco
    markdown_content = repo.read_note_content(note)
    if markdown_content is None:
        raise HTTPException(
            status_code=404,
            detail=f"Fichero no encontrado en disco para: {note_id}",
        )

    # Renderizar Markdown a HTML
    rendered_html = render(markdown_content, note_id=note_id)
    rendered_html = add_heading_anchors(rendered_html)

    # Construir TOC
    toc_html = _build_toc_html(note.headings)

    # Determinar el proceso de contexto
    current_process = process or (note.processes[0] if note.processes else "")
    process_title = note_service.format_process_title(current_process) if current_process else ""

    # Navegación secuencial (anterior / siguiente)
    prev_note, next_note = note_service.get_adjacent_notes(note, current_process or None)

    # Calcular posición y progreso
    if current_process:
        process_notes = note_service.sort_sequentially(
            note_service.get_by_process(current_process)
        )
        total_in_process = len(process_notes)
        position = next(
            (i + 1 for i, n in enumerate(process_notes) if n.id == note.id),
            0,
        )
        progress_percent = (position / total_in_process * 100) if total_in_process > 0 else 0
    else:
        total_in_process = 0
        position = 0
        progress_percent = 0

    # URL de práctica en Preparador TAI
    practice_url = _build_practice_url(note, note_service)

    # Tiempo de lectura
    reading_time = note_service.estimate_reading_time(note)

    return templates.TemplateResponse(
        request=request,
        name="note.html",
        context={
            "note": note,
            "rendered_html": rendered_html,
            "toc_html": toc_html,
            "process_title": process_title,
            "current_process": current_process,
            "prev_note": prev_note,
            "next_note": next_note,
            "position": position,
            "total_in_process": total_in_process,
            "progress_percent": progress_percent,
            "practice_url": practice_url,
            "reading_time": reading_time,
        },
    )


def _build_practice_url(note, note_service) -> str | None:
    """Construye la URL de práctica temática en Preparador TAI."""
    from config import PREPARADORTAI_BASE_URL

    topics = note_service.extract_practice_topics(note)
    if not topics:
        return None

    topics_param = "+".join(str(t) for t in topics)
    return (
        f"{PREPARADORTAI_BASE_URL}/practica_tematica.php"
        f"?topics={topics_param}&source=studyassistant"
    )


# ---------------------------------------------------------------------------
# API JSON para consumo entre servicios (linking-service, etc.)
# ---------------------------------------------------------------------------

@router.get("/api/notes")
async def list_notes_api(request: Request, process: str = ""):
    """Devuelve el catálogo de notas en formato JSON, opcionalmente filtrado por proceso."""
    note_service = request.app.state.note_service
    notes = note_service.filter_notes(process=process) if process else list(note_service.notes)
    return [
        {
            "id": n.id,
            "title": n.title,
            "official_topic": n.official_topic,
            "block": n.block,
            "processes": n.processes,
            "path": n.path,
        }
        for n in notes
    ]


@router.get("/api/notes/{note_id}")
async def get_note_api(request: Request, note_id: str):
    """Devuelve los metadatos de una nota en formato JSON."""
    note_service = request.app.state.note_service
    n = note_service.find_by_id(note_id)
    if not n:
        raise HTTPException(status_code=404, detail=f"Nota {note_id} no encontrada")
    return {
        "id": n.id,
        "title": n.title,
        "official_topic": n.official_topic,
        "block": n.block,
        "processes": n.processes,
        "path": n.path,
    }


