"""Escrituras y consultas de la gestión de preguntas y cuestionarios."""

from __future__ import annotations

import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session

from domain.management.forms import ExamInput, QuestionInput, ValidationError

MANUAL_SOURCE = "manual"
PAGE_SIZE = 50


class ManagementRepository:
    def __init__(self, session: Session) -> None:
        self._s = session

    # ------------------------------------------------------------------
    # Catálogos para los formularios
    # ------------------------------------------------------------------

    def syllabi(self) -> list[dict]:
        return [dict(r._mapping) for r in self._s.execute(text(
            "SELECT id, name, organism FROM syllabi ORDER BY organism, name"))]

    def scoring_rules(self) -> list[dict]:
        return [dict(r._mapping) for r in self._s.execute(text("SELECT id, code, name FROM scoring_rules ORDER BY id"))]

    def exams(self) -> list[dict]:
        return [dict(r._mapping) for r in self._s.execute(text(
            "SELECT e.id, e.name, e.year, e.convocatoria, e.syllabus_id, s.name AS syllabus_name, "
            "e.scoring_rule_id, r.name AS rule_name, e.duration_seconds, "
            "(SELECT COUNT(*) FROM exam_questions eq WHERE eq.exam_id = e.id) AS n_questions, "
            "(SELECT COUNT(*) FROM test_sessions ts WHERE ts.exam_id = e.id) AS n_sessions "
            "FROM exams e LEFT JOIN syllabi s ON s.id = e.syllabus_id "
            "LEFT JOIN scoring_rules r ON r.id = e.scoring_rule_id "
            "ORDER BY s.name, e.year DESC, e.name"))]

    # ------------------------------------------------------------------
    # Preguntas
    # ------------------------------------------------------------------

    def search_questions(self, *, q: str | None = None, syllabus_id: str | None = None,
                         exam_id: int | None = None, page: int = 1) -> tuple[list[dict], int]:
        where, params = ["1 = 1"], {}
        if q:
            where.append("q.statement LIKE :q")
            params["q"] = f"%{q.strip()}%"
        if syllabus_id:
            where.append("EXISTS (SELECT 1 FROM question_syllabus_tags t WHERE t.question_id = q.id AND t.syllabus_id = :s)")
            params["s"] = syllabus_id
        if exam_id:
            where.append("EXISTS (SELECT 1 FROM exam_questions eq WHERE eq.question_id = q.id AND eq.exam_id = :e)")
            params["e"] = exam_id
        cond = " AND ".join(where)
        total = self._s.execute(text(f"SELECT COUNT(*) FROM questions q WHERE {cond}"), params).scalar() or 0
        params.update(limit=PAGE_SIZE, offset=(max(page, 1) - 1) * PAGE_SIZE)
        rows = self._s.execute(text(
            f"SELECT q.id, q.statement, q.source, q.year, q.is_annulled, q.pending_classification, "
            f"(SELECT GROUP_CONCAT(t.syllabus_id || COALESCE(' ' || t.block, '') || COALESCE('·' || t.topic, ''), ', ') "
            f" FROM question_syllabus_tags t WHERE t.question_id = q.id) AS tags, "
            f"(SELECT COUNT(*) FROM test_attempts a WHERE a.question_id = q.id) AS n_attempts "
            f"FROM questions q WHERE {cond} ORDER BY q.id DESC LIMIT :limit OFFSET :offset"
        ), params)
        return [dict(r._mapping) for r in rows], int(total)

    def get_question(self, question_id: int) -> dict | None:
        row = self._s.execute(text("SELECT * FROM questions WHERE id = :i"), {"i": question_id}).first()
        if row is None:
            return None
        q = dict(row._mapping)
        q["options"] = [dict(r._mapping) for r in self._s.execute(text(
            "SELECT o.id, o.option_text, o.is_correct, o.display_order, o.justification, "
            "(SELECT COUNT(*) FROM test_attempts a WHERE a.selected_option_id = o.id) AS n_attempts "
            "FROM question_options o WHERE o.question_id = :i ORDER BY o.display_order, o.id"), {"i": question_id})]
        q["tags"] = [dict(r._mapping) for r in self._s.execute(text(
            "SELECT syllabus_id, block, topic FROM question_syllabus_tags WHERE question_id = :i ORDER BY id"),
            {"i": question_id})]
        q["exams"] = [dict(r._mapping) for r in self._s.execute(text(
            "SELECT e.id, e.name, eq.position, eq.is_reserve FROM exam_questions eq JOIN exams e ON e.id = eq.exam_id "
            "WHERE eq.question_id = :i ORDER BY e.name"), {"i": question_id})]
        q["n_attempts"] = self._s.execute(text(
            "SELECT COUNT(*) FROM test_attempts WHERE question_id = :i"), {"i": question_id}).scalar() or 0
        return q

    def create_question(self, data: QuestionInput) -> int:
        data.validate()
        qid = self._s.execute(text(
            "INSERT INTO questions (statement, justification, img_path, source, source_id, is_annulled, "
            "annulment_reason, pending_classification, year, is_official_exam) "
            "VALUES (:st, :j, NULL, :src, :sid, :ann, :reason, :pending, :year, :official)"
        ), self._question_params(data) | {"src": MANUAL_SOURCE, "sid": f"manual-{uuid.uuid4().hex[:12]}"}).lastrowid
        for order, opt in enumerate(data.options):
            self._insert_option(qid, opt, order, order == data.correct_index)
        self._set_tag(qid, data)
        if data.add_to_exam_id:
            self.add_to_exam(data.add_to_exam_id, qid)
        return qid

    def update_question(self, question_id: int, data: QuestionInput) -> None:
        data.validate()
        current = self.get_question(question_id)
        if current is None:
            raise ValidationError(["La pregunta no existe."])
        existing = {o["id"]: o for o in current["options"]}
        kept_ids = {o.option_id for o in data.options if o.option_id}
        unknown = kept_ids - existing.keys()
        if unknown:
            raise ValidationError(["Una de las opciones no pertenece a esta pregunta."])
        removed = [o for oid, o in existing.items() if oid not in kept_ids]
        blocked = [o["option_text"][:60] for o in removed if o["n_attempts"]]
        if blocked:
            raise ValidationError([f"No se puede quitar «{t}»: ya se ha elegido en algún intento." for t in blocked])

        self._s.execute(text(
            "UPDATE questions SET statement = :st, justification = :j, is_annulled = :ann, annulment_reason = :reason, "
            "pending_classification = :pending, year = :year, is_official_exam = :official WHERE id = :id"
        ), self._question_params(data) | {"id": question_id})
        for o in removed:
            self._s.execute(text("DELETE FROM question_options WHERE id = :i"), {"i": o["id"]})
        for order, opt in enumerate(data.options):
            is_correct = order == data.correct_index
            if opt.option_id:
                self._s.execute(text(
                    "UPDATE question_options SET option_text = :t, justification = :j, is_correct = :c, "
                    "display_order = :o WHERE id = :i AND question_id = :q"
                ), {"t": opt.text.strip(), "j": _clean(opt.justification), "c": int(is_correct), "o": order,
                    "i": opt.option_id, "q": question_id})
            else:
                self._insert_option(question_id, opt, order, is_correct)
        self._set_tag(question_id, data)
        if data.add_to_exam_id:
            self.add_to_exam(data.add_to_exam_id, question_id)

    def delete_question(self, question_id: int) -> None:
        n = self._s.execute(text("SELECT COUNT(*) FROM test_attempts WHERE question_id = :i"), {"i": question_id}).scalar()
        if n:
            raise ValidationError([f"Esta pregunta tiene {n} respuestas en tu historial: anúlala en vez de borrarla."])
        for table in ("question_options", "question_syllabus_tags", "exam_questions"):
            self._s.execute(text(f"DELETE FROM {table} WHERE question_id = :i"), {"i": question_id})
        self._s.execute(text("DELETE FROM questions WHERE id = :i"), {"i": question_id})

    def _question_params(self, data: QuestionInput) -> dict:
        return {
            "st": data.statement.strip(), "j": _clean(data.justification),
            "ann": int(data.is_annulled), "reason": _clean(data.annulment_reason) if data.is_annulled else None,
            "pending": int(not data.block), "year": data.year, "official": int(data.is_official_exam),
        }

    def _insert_option(self, question_id: int, opt, order: int, is_correct: bool) -> None:
        self._s.execute(text(
            "INSERT INTO question_options (question_id, option_text, is_correct, display_order, justification) "
            "VALUES (:q, :t, :c, :o, :j)"
        ), {"q": question_id, "t": opt.text.strip(), "c": int(is_correct), "o": order, "j": _clean(opt.justification)})

    def _set_tag(self, question_id: int, data: QuestionInput) -> None:
        """Una etiqueta por temario: se reemplaza la del temario elegido; las de otros temarios no se tocan."""
        self._s.execute(text("DELETE FROM question_syllabus_tags WHERE question_id = :q AND syllabus_id = :s"),
                        {"q": question_id, "s": data.syllabus_id})
        self._s.execute(text(
            "INSERT INTO question_syllabus_tags (question_id, syllabus_id, block, topic) VALUES (:q, :s, :b, :t)"
        ), {"q": question_id, "s": data.syllabus_id, "b": _clean(data.block), "t": _clean(data.topic)})

    # ------------------------------------------------------------------
    # Cuestionarios
    # ------------------------------------------------------------------

    def get_exam(self, exam_id: int) -> dict | None:
        row = self._s.execute(text("SELECT * FROM exams WHERE id = :i"), {"i": exam_id}).first()
        if row is None:
            return None
        exam = dict(row._mapping)
        exam["questions"] = [dict(r._mapping) for r in self._s.execute(text(
            "SELECT q.id, q.statement, q.is_annulled, eq.position, eq.is_reserve FROM exam_questions eq "
            "JOIN questions q ON q.id = eq.question_id WHERE eq.exam_id = :i ORDER BY eq.position"), {"i": exam_id})]
        exam["n_sessions"] = self._s.execute(text(
            "SELECT COUNT(*) FROM test_sessions WHERE exam_id = :i"), {"i": exam_id}).scalar() or 0
        return exam

    def save_exam(self, data: ExamInput, exam_id: int | None = None) -> int:
        data.validate()
        clash = self._s.execute(text(
            "SELECT id FROM exams WHERE name = :n AND syllabus_id = :s AND id != COALESCE(:i, -1)"
        ), {"n": data.name.strip(), "s": data.syllabus_id, "i": exam_id}).first()
        if clash:
            raise ValidationError(["Ya existe un cuestionario con ese nombre en ese temario."])
        params = {
            "n": data.name.strip(), "y": data.year, "c": _clean(data.convocatoria), "s": data.syllabus_id,
            "r": data.scoring_rule_id, "d": data.duration_minutes * 60 if data.duration_minutes else None,
        }
        if exam_id is None:
            return self._s.execute(text(
                "INSERT INTO exams (name, year, convocatoria, syllabus_id, scoring_rule_id, duration_seconds) "
                "VALUES (:n, :y, :c, :s, :r, :d)"), params).lastrowid
        self._s.execute(text(
            "UPDATE exams SET name = :n, year = :y, convocatoria = :c, syllabus_id = :s, scoring_rule_id = :r, "
            "duration_seconds = :d WHERE id = :i"), params | {"i": exam_id})
        return exam_id

    def delete_exam(self, exam_id: int) -> None:
        n = self._s.execute(text("SELECT COUNT(*) FROM test_sessions WHERE exam_id = :i"), {"i": exam_id}).scalar()
        if n:
            raise ValidationError([f"Este cuestionario tiene {n} sesiones en tu historial: no se puede borrar."])
        self._s.execute(text("DELETE FROM exam_questions WHERE exam_id = :i"), {"i": exam_id})
        self._s.execute(text("DELETE FROM exams WHERE id = :i"), {"i": exam_id})

    def add_to_exam(self, exam_id: int, question_id: int) -> None:
        if self._s.execute(text("SELECT 1 FROM exams WHERE id = :e"), {"e": exam_id}).first() is None:
            raise ValidationError(["El cuestionario no existe."])
        if self._s.execute(text("SELECT 1 FROM exam_questions WHERE exam_id = :e AND question_id = :q"),
                           {"e": exam_id, "q": question_id}).first():
            return
        position = (self._s.execute(text("SELECT MAX(position) FROM exam_questions WHERE exam_id = :e"),
                                    {"e": exam_id}).scalar() or 0) + 1
        self._s.execute(text(
            "INSERT INTO exam_questions (exam_id, question_id, position, is_reserve) VALUES (:e, :q, :p, 0)"
        ), {"e": exam_id, "q": question_id, "p": position})

    def remove_from_exam(self, exam_id: int, question_id: int) -> None:
        self._s.execute(text("DELETE FROM exam_questions WHERE exam_id = :e AND question_id = :q"),
                        {"e": exam_id, "q": question_id})


def _clean(value: str | None) -> str | None:
    value = (value or "").strip()
    return value or None
