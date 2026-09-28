"""Rutas del dashboard principal y catálogo de apuntes."""

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    q: str = Query("", description="Texto de búsqueda"),
    tag: str = Query("", description="Filtro por etiqueta"),
    process: str = Query("", description="Filtro por proceso selectivo"),
    status: str = Query("", description="Filtro por estado"),
):
    """Dashboard principal: KPIs, Process Hub, catálogo de apuntes con filtros."""
    from domain.notes.service import NoteService

    note_service: NoteService = request.app.state.note_service
    templates = request.app.state.templates

    # Filtrar notas si hay criterios activos
    is_filtered = any([q, tag, process, status])
    if is_filtered:
        filtered_notes = note_service.filter_notes(
            query=q, tag=tag, process=process, status=status
        )
    else:
        filtered_notes = list(note_service.notes)

    # Agrupar por proceso
    notes_by_process: dict[str, list] = {}
    for note in filtered_notes:
        procs = note.processes if note.processes else ["sin-proceso"]
        for proc in procs:
            notes_by_process.setdefault(proc, []).append(note)

    # Ordenar cada grupo secuencialmente
    for proc_slug in notes_by_process:
        notes_by_process[proc_slug] = note_service.sort_sequentially(
            notes_by_process[proc_slug]
        )

    # Títulos formateados de procesos
    process_titles = {
        slug: note_service.format_process_title(slug)
        for slug in notes_by_process
    }

    # Métricas del dashboard
    metrics = note_service.get_dashboard_metrics()

    # Filtros activos (chips con botón ×)
    active_filters = _build_active_filters(q, tag, process, status)

    # Facetas para dropdowns
    all_tags = note_service.collect_unique("tags")
    all_processes = note_service.collect_unique("processes")
    all_statuses = note_service.collect_statuses()

    # Limitar vista previa si no hay filtros (6 por proceso)
    if not is_filtered:
        for proc_slug in notes_by_process:
            if len(notes_by_process[proc_slug]) > 6:
                notes_by_process[proc_slug] = notes_by_process[proc_slug][:6]

    total_filtered = sum(len(notes) for notes in notes_by_process.values())

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "metrics": metrics,
            "notes_by_process": notes_by_process,
            "process_titles": process_titles,
            "query": q,
            "tag": tag,
            "process": process,
            "status": status,
            "active_filters": active_filters,
            "all_tags": all_tags,
            "all_processes": all_processes,
            "all_statuses": all_statuses,
            "is_filtered": is_filtered,
            "total_filtered": total_filtered,
        },
    )


def _build_active_filters(
    query: str, tag: str, process: str, status: str
) -> list[dict]:
    """Construye la lista de chips de filtros activos con URL de eliminación."""
    filters = []
    params = {"q": query, "tag": tag, "process": process, "status": status}

    if query:
        remove_params = {k: v for k, v in params.items() if k != "q" and v}
        remove_url = "/?" + "&".join(f"{k}={v}" for k, v in remove_params.items()) if remove_params else "/"
        filters.append({"name": "Búsqueda", "value": query, "remove_url": remove_url})

    if tag:
        remove_params = {k: v for k, v in params.items() if k != "tag" and v}
        remove_url = "/?" + "&".join(f"{k}={v}" for k, v in remove_params.items()) if remove_params else "/"
        filters.append({"name": "Etiqueta", "value": tag, "remove_url": remove_url})

    if process:
        remove_params = {k: v for k, v in params.items() if k != "process" and v}
        remove_url = "/?" + "&".join(f"{k}={v}" for k, v in remove_params.items()) if remove_params else "/"
        filters.append({"name": "Proceso", "value": process, "remove_url": remove_url})

    if status:
        remove_params = {k: v for k, v in params.items() if k != "status" and v}
        remove_url = "/?" + "&".join(f"{k}={v}" for k, v in remove_params.items()) if remove_params else "/"
        filters.append({"name": "Estado", "value": status, "remove_url": remove_url})

    return filters

