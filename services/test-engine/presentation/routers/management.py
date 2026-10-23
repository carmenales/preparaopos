"""Gestión de preguntas y cuestionarios (sustituye a gestionar, agregar, editar,
categorias, nueva_categoria y editar_cuestionario de preparadortai)."""

from __future__ import annotations

from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

import config
from config import prefix_url
from domain.management.forms import MAX_OPTIONS, ExamInput, OptionInput, QuestionInput, ValidationError
from infrastructure.db.repositories.management_repository import PAGE_SIZE, ManagementRepository
from presentation.dependencies import DbDep, LinkingClientDep, NotesCatalogDep
from presentation.templating import templates

router = APIRouter(prefix="/manage")
NO_CACHE = {"Cache-Control": "no-store"}


def get_repo(db: DbDep) -> ManagementRepository:
    return ManagementRepository(db)


RepoDep = Annotated[ManagementRepository, Depends(get_repo)]


def _int(value: str | None) -> int | None:
    value = (value or "").strip()
    return int(value) if value.isdigit() else None


def _redirect(path: str, **params) -> RedirectResponse:
    query = urlencode({k: v for k, v in params.items() if v not in (None, "")})
    return RedirectResponse(url=prefix_url(path + (f"?{query}" if query else "")), status_code=303)


# ---------------------------------------------------------------------------
# Preguntas
# ---------------------------------------------------------------------------

@router.get("/questions/", response_class=HTMLResponse)
def list_questions(request: Request, repo: RepoDep, q: str | None = None, syllabus_id: str | None = None,
                   exam_id: str | None = None, page: str | None = None, msg: str | None = None):
    page_n = max(_int(page) or 1, 1)
    rows, total = repo.search_questions(q=q, syllabus_id=syllabus_id or None, exam_id=_int(exam_id), page=page_n)
    filters = {"q": q or "", "syllabus_id": syllabus_id or "", "exam_id": exam_id or ""}
    return templates.TemplateResponse(request, "manage_questions.html", {
        "rows": rows, "total": total, "page": page_n, "pages": max((total + PAGE_SIZE - 1) // PAGE_SIZE, 1),
        "filters": filters, "query": urlencode({k: v for k, v in filters.items() if v}),
        "syllabi": repo.syllabi(), "exams": repo.exams(), "msg": msg,
    }, headers=NO_CACHE)


LINK_SOURCES = {"manual": "a mano", "topic-match": "automático por tema",
                "semantic-suggestion": "sugerencia automática"}


def _links_panel(question, linking, catalog) -> dict:
    """Datos de la sección «Apuntes enlazados». Cada servicio puede faltar sin romper la página."""
    links = linking.links_for_question(question["id"])
    notes = catalog.list_notes()
    groups = None
    if notes is not None:
        linked = {l["note_id"] for l in links or []}
        by_group: dict[str, list[dict]] = {}
        for n in notes:
            if n["id"] in linked:
                continue
            label = ", ".join(sorted(n.get("processes") or [])) or "Sin proceso"
            by_group.setdefault(label, []).append(n)
        groups = [(label, sorted(items, key=lambda n: ((n.get("official_topic") or "").lower(), n["title"].lower())))
                  for label, items in sorted(by_group.items())]
    return {"links": links, "groups": groups, "sources": LINK_SOURCES,
            "study_assistant_url": config.STUDY_ASSISTANT_PUBLIC_URL.rstrip("/")}


def _question_form(request, repo, *, question=None, values=None, errors=None, exam_id=None, msg=None,
                   status_code=200, links_panel=None):
    if values is None:
        if question:
            tag = question["tags"][0] if question["tags"] else {}
            values = {
                "statement": question["statement"], "justification": question["justification"] or "",
                "syllabus_id": tag.get("syllabus_id", ""), "block": tag.get("block") or "", "topic": tag.get("topic") or "",
                "year": question["year"] or "", "is_official_exam": bool(question["is_official_exam"]),
                "is_annulled": bool(question["is_annulled"]), "annulment_reason": question["annulment_reason"] or "",
                "options": [{"id": o["id"], "text": o["option_text"], "justification": o["justification"] or "",
                             "n_attempts": o["n_attempts"]} for o in question["options"]],
                "correct": next((i for i, o in enumerate(question["options"]) if o["is_correct"]), None),
                "add_to_exam_id": "",
            }
        else:
            values = {"statement": "", "justification": "", "syllabus_id": "", "block": "", "topic": "", "year": "",
                      "is_official_exam": False, "is_annulled": False, "annulment_reason": "", "options": [],
                      "correct": None, "add_to_exam_id": str(exam_id or "")}
    rows = values["options"] + [{"id": "", "text": "", "justification": "", "n_attempts": 0}] * (
        MAX_OPTIONS - len(values["options"]))
    values = values | {"options": rows[:MAX_OPTIONS]}
    return templates.TemplateResponse(request, "manage_question_form.html", {
        "question": question, "v": values, "errors": errors or [], "msg": msg,
        "syllabi": repo.syllabi(), "exams": repo.exams(), "lp": links_panel,
    }, status_code=status_code, headers=NO_CACHE)


def _parse_question(statement, justification, syllabus_id, block, topic, year, is_official_exam, is_annulled,
                    annulment_reason, opt_id, opt_text, opt_just, correct, add_to_exam_id):
    options, correct_index, raw_rows = [], None, []
    for row, (oid, txt, just) in enumerate(zip(opt_id, opt_text, opt_just)):
        raw_rows.append({"id": _int(oid) or "", "text": txt, "justification": just, "n_attempts": 0})
        if txt.strip():
            if str(row) == correct:
                correct_index = len(options)
            options.append(OptionInput(text=txt, justification=just, option_id=_int(oid)))
    data = QuestionInput(
        statement=statement, options=options, correct_index=correct_index, justification=justification,
        syllabus_id=syllabus_id or None, block=block, topic=topic, year=_int(year),
        is_official_exam=bool(is_official_exam), is_annulled=bool(is_annulled), annulment_reason=annulment_reason,
        add_to_exam_id=_int(add_to_exam_id),
    )
    values = {"statement": statement, "justification": justification, "syllabus_id": syllabus_id, "block": block,
              "topic": topic, "year": year, "is_official_exam": bool(is_official_exam),
              "is_annulled": bool(is_annulled), "annulment_reason": annulment_reason,
              "options": raw_rows,  # tal cual llegaron, para que «correct» siga apuntando a su fila
              "correct": _int(correct), "add_to_exam_id": add_to_exam_id}
    return data, values


@router.get("/questions/new", response_class=HTMLResponse)
def new_question(request: Request, repo: RepoDep, exam_id: str | None = None):
    return _question_form(request, repo, exam_id=_int(exam_id))


@router.get("/questions/{question_id}/edit", response_class=HTMLResponse)
def edit_question(request: Request, question_id: int, repo: RepoDep, linking: LinkingClientDep,
                  catalog: NotesCatalogDep, msg: str | None = None):
    question = repo.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return _question_form(request, repo, question=question, msg=msg,
                          links_panel=_links_panel(question, linking, catalog))


def _save_question(request, repo, question_id, form_args, links_panel=None):
    data, values = _parse_question(**form_args)
    question = repo.get_question(question_id) if question_id else None
    try:
        if question_id:
            repo.update_question(question_id, data)
            saved_id = question_id
        else:
            saved_id = repo.create_question(data)
    except ValidationError as exc:
        if question:
            attempts = {o["id"]: o["n_attempts"] for o in question["options"]}
            for o in values["options"]:
                o["n_attempts"] = attempts.get(o["id"], 0)
        return _question_form(request, repo, question=question, values=values, errors=exc.errors, status_code=422,
                              links_panel=links_panel(question) if links_panel and question else None)
    return _redirect(f"/manage/questions/{saved_id}/edit", msg="Pregunta guardada.")


def _form_fields(
    statement: Annotated[str, Form()] = "",
    justification: Annotated[str, Form()] = "",
    syllabus_id: Annotated[str, Form()] = "",
    block: Annotated[str, Form()] = "",
    topic: Annotated[str, Form()] = "",
    year: Annotated[str, Form()] = "",
    is_official_exam: Annotated[str | None, Form()] = None,
    is_annulled: Annotated[str | None, Form()] = None,
    annulment_reason: Annotated[str, Form()] = "",
    opt_id: Annotated[list[str], Form()] = [],
    opt_text: Annotated[list[str], Form()] = [],
    opt_just: Annotated[list[str], Form()] = [],
    correct: Annotated[str, Form()] = "",
    add_to_exam_id: Annotated[str, Form()] = "",
) -> dict:
    return dict(statement=statement, justification=justification, syllabus_id=syllabus_id, block=block, topic=topic,
                year=year, is_official_exam=is_official_exam, is_annulled=is_annulled,
                annulment_reason=annulment_reason, opt_id=opt_id, opt_text=opt_text, opt_just=opt_just,
                correct=correct, add_to_exam_id=add_to_exam_id)


FormDep = Annotated[dict, Depends(_form_fields)]


@router.post("/questions/new", response_class=HTMLResponse)
def create_question(request: Request, repo: RepoDep, form: FormDep):
    return _save_question(request, repo, None, form)


@router.post("/questions/{question_id}/edit", response_class=HTMLResponse)
def update_question(request: Request, question_id: int, repo: RepoDep, form: FormDep, linking: LinkingClientDep,
                    catalog: NotesCatalogDep):
    if repo.get_question(question_id) is None:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return _save_question(request, repo, question_id, form,
                          links_panel=lambda q: _links_panel(q, linking, catalog))


# Enlaces pregunta-apunte: los guarda linking-service; aquí solo se editan a mano.
# Handlers síncronos porque el cliente HTTP es síncrono.

@router.post("/questions/{question_id}/links/add", response_class=HTMLResponse)
def add_question_link(question_id: int, repo: RepoDep, linking: LinkingClientDep,
                      note_id: Annotated[str, Form()] = ""):
    question = repo.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    note_id = note_id.strip()
    if not note_id:
        return _redirect(f"/manage/questions/{question_id}/edit", msg="No se ha podido enlazar: elige un apunte.")
    syllabus_id = question["tags"][0]["syllabus_id"] if question["tags"] else "manual"
    error = linking.add_link(question_id, note_id, syllabus_id)
    msg = f"No se ha podido enlazar: {error}" if error else "Apunte enlazado."
    return _redirect(f"/manage/questions/{question_id}/edit", msg=msg)


@router.post("/questions/{question_id}/links/remove", response_class=HTMLResponse)
def remove_question_link(question_id: int, repo: RepoDep, linking: LinkingClientDep,
                         note_id: Annotated[str, Form()] = ""):
    if repo.get_question(question_id) is None:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    error = linking.remove_link(question_id, note_id.strip()) if note_id.strip() else "falta el apunte."
    msg = f"No se ha podido quitar el enlace: {error}" if error else "Enlace quitado."
    return _redirect(f"/manage/questions/{question_id}/edit", msg=msg)


@router.post("/questions/{question_id}/delete", response_class=HTMLResponse)
def delete_question(request: Request, question_id: int, repo: RepoDep):
    try:
        repo.delete_question(question_id)
    except ValidationError as exc:
        return _redirect(f"/manage/questions/{question_id}/edit", msg=exc.errors[0])
    return _redirect("/manage/questions/", msg="Pregunta borrada.")


# ---------------------------------------------------------------------------
# Cuestionarios
# ---------------------------------------------------------------------------

@router.get("/exams/", response_class=HTMLResponse)
def list_exams(request: Request, repo: RepoDep, msg: str | None = None):
    return templates.TemplateResponse(request, "manage_exams.html", {"exams": repo.exams(), "msg": msg},
                                      headers=NO_CACHE)


def _exam_form(request, repo, *, exam=None, values=None, errors=None, msg=None, status_code=200):
    if values is None:
        values = ({"name": exam["name"], "syllabus_id": exam["syllabus_id"] or "", "year": exam["year"] or "",
                   "convocatoria": exam["convocatoria"] or "", "scoring_rule_id": exam["scoring_rule_id"] or "",
                   "duration_minutes": (exam["duration_seconds"] // 60) if exam["duration_seconds"] else ""}
                  if exam else {"name": "", "syllabus_id": "", "year": "", "convocatoria": "", "scoring_rule_id": "",
                                "duration_minutes": ""})
    return templates.TemplateResponse(request, "manage_exam_form.html", {
        "exam": exam, "v": values, "errors": errors or [], "msg": msg,
        "syllabi": repo.syllabi(), "rules": repo.scoring_rules(),
    }, status_code=status_code, headers=NO_CACHE)


def _exam_fields(
    name: Annotated[str, Form()] = "",
    syllabus_id: Annotated[str, Form()] = "",
    year: Annotated[str, Form()] = "",
    convocatoria: Annotated[str, Form()] = "",
    scoring_rule_id: Annotated[str, Form()] = "",
    duration_minutes: Annotated[str, Form()] = "",
) -> dict:
    return dict(name=name, syllabus_id=syllabus_id, year=year, convocatoria=convocatoria,
                scoring_rule_id=scoring_rule_id, duration_minutes=duration_minutes)


ExamFormDep = Annotated[dict, Depends(_exam_fields)]


def _save_exam(request, repo, exam_id, form):
    data = ExamInput(name=form["name"], syllabus_id=form["syllabus_id"] or None, year=_int(form["year"]),
                     convocatoria=form["convocatoria"], scoring_rule_id=_int(form["scoring_rule_id"]),
                     duration_minutes=_int(form["duration_minutes"]))
    try:
        saved = repo.save_exam(data, exam_id)
    except ValidationError as exc:
        exam = repo.get_exam(exam_id) if exam_id else None
        return _exam_form(request, repo, exam=exam, values=form, errors=exc.errors, status_code=422)
    return _redirect(f"/manage/exams/{saved}/edit", msg="Cuestionario guardado.")


@router.get("/exams/new", response_class=HTMLResponse)
def new_exam(request: Request, repo: RepoDep):
    return _exam_form(request, repo)


@router.post("/exams/new", response_class=HTMLResponse)
def create_exam(request: Request, repo: RepoDep, form: ExamFormDep):
    return _save_exam(request, repo, None, form)


@router.get("/exams/{exam_id}/edit", response_class=HTMLResponse)
def edit_exam(request: Request, exam_id: int, repo: RepoDep, msg: str | None = None):
    exam = repo.get_exam(exam_id)
    if exam is None:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    return _exam_form(request, repo, exam=exam, msg=msg)


@router.post("/exams/{exam_id}/edit", response_class=HTMLResponse)
def update_exam(request: Request, exam_id: int, repo: RepoDep, form: ExamFormDep):
    if repo.get_exam(exam_id) is None:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    return _save_exam(request, repo, exam_id, form)


@router.post("/exams/{exam_id}/delete", response_class=HTMLResponse)
def delete_exam(exam_id: int, repo: RepoDep):
    try:
        repo.delete_exam(exam_id)
    except ValidationError as exc:
        return _redirect(f"/manage/exams/{exam_id}/edit", msg=exc.errors[0])
    return _redirect("/manage/exams/", msg="Cuestionario borrado.")


@router.post("/exams/{exam_id}/questions/{question_id}/remove", response_class=HTMLResponse)
def remove_from_exam(exam_id: int, question_id: int, repo: RepoDep):
    repo.remove_from_exam(exam_id, question_id)
    return _redirect(f"/manage/exams/{exam_id}/edit", msg="Pregunta quitada del cuestionario (no se ha borrado).")
