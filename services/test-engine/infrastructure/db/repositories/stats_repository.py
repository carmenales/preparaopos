"""Consultas de lectura para el historial de sesiones y las estadísticas."""

from __future__ import annotations

import json
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.orm import Session

from domain.sessions.collections import fixed_test_title
from domain.sessions.generator import GeneratorFilters
from domain.stats.insights import direction, priority_label, priority_score, trend

# Pregunta fallada pendiente = su último intento respondido fue incorrecto
# (misma definición que el refuerzo del generador).
_LAST_ANSWER_SQL = """
    SELECT a.question_id, a.is_correct FROM test_attempts a
    WHERE a.selected_option_id IS NOT NULL
      AND a.answered_at = (
          SELECT MAX(b.answered_at) FROM test_attempts b
          WHERE b.question_id = a.question_id AND b.selected_option_id IS NOT NULL
      )
"""


def _pct(part: int, total: int) -> float | None:
    return round(100 * part / total, 1) if total else None


class StatsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Historial
    # ------------------------------------------------------------------

    def list_sessions(self, limit: int = 300) -> list[dict]:
        syllabus_names = dict(self._session.execute(text("SELECT id, name FROM syllabi")).fetchall())
        rows = self._session.execute(text(
            "SELECT s.id, s.mode, s.source, s.source_ref, s.started_at, s.closed_at, s.status, "
            "s.final_score, s.question_ids, s.duration_seconds, e.name AS exam_name, "
            "COALESCE(SUM(CASE WHEN a.selected_option_id IS NOT NULL THEN 1 ELSE 0 END), 0) AS answered, "
            "COALESCE(SUM(CASE WHEN a.selected_option_id IS NOT NULL AND a.is_correct = 1 THEN 1 ELSE 0 END), 0) AS correct "
            "FROM test_sessions s "
            "LEFT JOIN exams e ON e.id = s.exam_id "
            "LEFT JOIN test_attempts a ON a.test_session_id = s.id "
            "GROUP BY s.id ORDER BY s.started_at DESC LIMIT :limit"
        ), {"limit": limit}).fetchall()

        sessions = []
        for r in rows:
            total = len(json.loads(r.question_ids or "[]"))
            sessions.append({
                "id": r.id,
                "mode": r.mode,
                "source": r.source,
                "label": self._label(r, syllabus_names),
                "started_at": str(r.started_at)[:16],
                "is_closed": r.closed_at is not None,
                "final_score": Decimal(str(r.final_score)) if r.final_score is not None else None,
                "total": total,
                "answered": r.answered,
                "correct": r.correct,
                "wrong": r.answered - r.correct,
                "blank": max(total - r.answered, 0),
            })
        return sessions

    def session_label(self, session_id: str) -> str | None:
        """Nombre legible de un test (el mismo que en el historial): examen, generado, apunte..."""
        row = self._session.execute(text(
            "SELECT s.source, s.source_ref, e.name AS exam_name FROM test_sessions s "
            "LEFT JOIN exams e ON e.id = s.exam_id WHERE s.id = :id"
        ), {"id": session_id}).fetchone()
        if row is None:
            return None
        syllabus_names = dict(self._session.execute(text("SELECT id, name FROM syllabi")).fetchall())
        return self._label(row, syllabus_names)

    @staticmethod
    def _label(row, syllabus_names: dict[str, str]) -> str:
        ref = row.source_ref or ""
        if row.source == "exam":
            return row.exam_name or f"Examen {ref}"
        if row.source == "legacy":
            return ref.removeprefix("preparadortai: ") + " (preparadortai)"
        if row.source == "note":
            return f"Apunte: {ref}"
        if row.source == "generated":
            try:
                f = GeneratorFilters.from_source_ref(ref)
            except ValueError:
                return "Test generado"
            if f.part:  # test fijo de una colección (Aleatorios, Bloques...)
                return f"{syllabus_names.get(f.syllabus_id, f.syllabus_id)} · {fixed_test_title(f)}"
            parts = [syllabus_names.get(f.syllabus_id, f.syllabus_id)]
            if f.block:
                parts.append(f"Bloque {f.block}" + (f" · Tema {f.topic}" if f.topic else ""))
            if f.year:
                parts.append(str(f.year))
            if f.official_only:
                parts.append("solo examen oficial")
            if f.failed_only:
                parts.append("refuerzo")
            if f.doubtful_only:
                parts.append("dudosas")
            if f.weighted:
                parts.append("ponderado por frecuencia")
            return "Generado: " + " · ".join(parts)
        if row.source == "questions":
            return "Preguntas sueltas"
        return f"{row.source}: {ref}" if ref else row.source

    def fixed_test_status(self, source_refs: list[str]) -> dict[str, dict]:
        """Estado de cada test fijo: sesión sin terminar (para continuarla), veces hecho y nota de la última."""
        wanted = set(source_refs)
        rows = self._session.execute(text(
            "SELECT id, source_ref, closed_at, final_score FROM test_sessions "
            "WHERE source = 'generated' AND source_ref LIKE '%part=%' ORDER BY started_at"
        )).fetchall()
        status: dict[str, dict] = {}
        for r in rows:
            if r.source_ref not in wanted:
                continue
            s = status.setdefault(r.source_ref, {"open_id": None, "done": 0, "last_score": None})
            if r.closed_at is None:
                s["open_id"] = r.id
            else:
                s["done"] += 1
                s["last_score"] = float(r.final_score) if r.final_score is not None else None
        return status

    def _exam_progress(self, syllabus_id: str) -> list[dict]:
        """Progreso por examen del temario (el «Ranking de exámenes oficiales» de preparadortai)."""
        rows = self._session.execute(text(
            "SELECT e.id, e.name, e.year, s.final_score, s.closed_at FROM test_sessions s "
            "JOIN exams e ON e.id = s.exam_id "
            "WHERE e.syllabus_id = :s AND s.closed_at IS NOT NULL AND s.final_score IS NOT NULL "
            "ORDER BY s.closed_at"
        ), {"s": syllabus_id}).fetchall()
        exams: dict[int, dict] = {}
        for r in rows:
            e = exams.setdefault(r.id, {"id": r.id, "name": r.name, "year": r.year, "scores": [], "last_date": None})
            e["scores"].append(float(r.final_score))
            e["last_date"] = str(r.closed_at)[:10]
        result = []
        for e in exams.values():
            scores = e.pop("scores")
            delta = scores[-1] - scores[-2] if len(scores) > 1 else None
            result.append({**e, "attempts": len(scores), "best": max(scores), "last": scores[-1],
                           "delta": delta, "direction": direction(delta)})
        # Primero los que peor llevas: la última nota más baja.
        result.sort(key=lambda e: (e["last"], -e["attempts"]))
        return result

    def _recurrent_mistakes(self, attempts_sql: str, params: dict, limit: int = 15) -> list[dict]:
        """Preguntas falladas al menos dos veces (las «preguntas con fallos recurrentes» de preparadortai)."""
        rows = self._session.execute(text(
            "SELECT x.question_id, COUNT(*) AS attempts, SUM(1 - COALESCE(x.is_correct, 0)) AS wrong, "
            "MAX(x.answered_at) AS last_at FROM ("
            "  SELECT DISTINCT a.id, a.question_id, a.is_correct, a.answered_at FROM test_attempts a "
            "  JOIN question_syllabus_tags t ON t.question_id = a.question_id "
            "  WHERE t.syllabus_id = :s AND a.selected_option_id IS NOT NULL) x "
            "GROUP BY x.question_id HAVING wrong >= 2 "
            "ORDER BY wrong DESC, wrong * 1.0 / attempts DESC, last_at DESC LIMIT :limit"
        ), {**params, "limit": limit}).fetchall()
        if not rows:
            return []
        ids = [r.question_id for r in rows]
        marks = ",".join(str(i) for i in ids)
        info = {
            r.id: r for r in self._session.execute(text(
                f"SELECT q.id, q.statement, MIN(t.block) AS block, MIN(t.topic) AS topic FROM questions q "
                f"LEFT JOIN question_syllabus_tags t ON t.question_id = q.id AND t.syllabus_id = :s "
                f"WHERE q.id IN ({marks}) GROUP BY q.id"
            ), params)
        }
        last = {
            r.question_id: r.is_correct for r in self._session.execute(text(
                f"SELECT l.question_id, l.is_correct FROM ({_LAST_ANSWER_SQL}) l WHERE l.question_id IN ({marks})"
            ))
        }
        return [
            {"id": r.question_id, "statement": info[r.question_id].statement if r.question_id in info else "",
             "block": info[r.question_id].block if r.question_id in info else None,
             "topic": info[r.question_id].topic if r.question_id in info else None,
             "attempts": r.attempts, "wrong": int(r.wrong), "error": _pct(int(r.wrong), r.attempts),
             "last_correct": bool(last.get(r.question_id)), "last_date": str(r.last_at)[:10] if r.last_at else ""}
            for r in rows
        ]

    def delete_session(self, session_id: str) -> bool:
        """Borra la sesión y sus intentos (ON DELETE CASCADE). Devuelve si existía."""
        self._session.execute(text("DELETE FROM test_attempts WHERE test_session_id = :id"), {"id": session_id})
        result = self._session.execute(text("DELETE FROM test_sessions WHERE id = :id"), {"id": session_id})
        return result.rowcount > 0

    # ------------------------------------------------------------------
    # Estadísticas
    # ------------------------------------------------------------------

    def syllabi_with_activity(self) -> list[dict]:
        rows = self._session.execute(text(
            "SELECT s.id, s.name, s.organism, COUNT(a.id) AS answered "
            "FROM syllabi s JOIN question_syllabus_tags t ON t.syllabus_id = s.id "
            "JOIN test_attempts a ON a.question_id = t.question_id AND a.selected_option_id IS NOT NULL "
            "GROUP BY s.id ORDER BY answered DESC"
        )).fetchall()
        return [{"id": r.id, "name": r.name, "organism": r.organism, "answered": r.answered} for r in rows]

    def syllabus_stats(self, syllabus_id: str) -> dict:
        params = {"s": syllabus_id}
        # Una fila por intento respondido de una pregunta del temario. DISTINCT evita
        # contar dos veces un intento si la pregunta tuviera varias etiquetas del temario.
        attempts_sql = (
            "SELECT DISTINCT a.id, a.question_id, a.is_correct, a.test_session_id, t.block, t.topic "
            "FROM test_attempts a JOIN question_syllabus_tags t ON t.question_id = a.question_id "
            "WHERE t.syllabus_id = :s AND a.selected_option_id IS NOT NULL"
        )
        totals = self._session.execute(text(
            f"SELECT COUNT(*) AS answered, COALESCE(SUM(is_correct), 0) AS correct, "
            f"COUNT(DISTINCT question_id) AS questions, COUNT(DISTINCT test_session_id) AS sessions "
            f"FROM ({attempts_sql})"
        ), params).one()
        pool = self._session.execute(text(
            "SELECT COUNT(DISTINCT t.question_id) FROM question_syllabus_tags t "
            "JOIN questions q ON q.id = t.question_id WHERE t.syllabus_id = :s AND q.is_annulled = 0"
        ), params).scalar() or 0
        pending = self._session.execute(text(
            f"SELECT COUNT(DISTINCT l.question_id) FROM ({_LAST_ANSWER_SQL}) l "
            f"JOIN question_syllabus_tags t ON t.question_id = l.question_id "
            f"WHERE t.syllabus_id = :s AND l.is_correct = 0"
        ), params).scalar() or 0

        topic_rows = self._session.execute(text(
            f"SELECT block, topic, COUNT(*) AS answered, COALESCE(SUM(is_correct), 0) AS correct, "
            f"COUNT(DISTINCT question_id) AS questions FROM ({attempts_sql}) "
            f"GROUP BY block, topic"
        ), params).fetchall()
        pending_by_topic = {
            (r.block, r.topic): r.n for r in self._session.execute(text(
                f"SELECT t.block, t.topic, COUNT(DISTINCT l.question_id) AS n FROM ({_LAST_ANSWER_SQL}) l "
                f"JOIN question_syllabus_tags t ON t.question_id = l.question_id "
                f"WHERE t.syllabus_id = :s AND l.is_correct = 0 GROUP BY t.block, t.topic"
            ), params)
        }
        topics = [
            {
                "block": r.block,
                "topic": r.topic,
                "scope": (f"{r.block}|{r.topic}" if r.topic else r.block) if r.block else "",
                "answered": r.answered,
                "correct": r.correct,
                "questions": r.questions,
                "accuracy": _pct(r.correct, r.answered),
                "wrong": r.answered - r.correct,
                "pending": pending_by_topic.get((r.block, r.topic), 0),
                "priority": priority_label(r.answered, r.correct),
                "priority_score": priority_score(r.answered, r.correct),
            }
            for r in topic_rows
        ]
        # Como el «Diagnóstico de áreas débiles» de preparadortai: primero lo que más conviene repasar
        # (fallos × lo que falta para el 100 %); a igualdad, lo que tiene más respuestas.
        topics.sort(key=lambda t: (-t["priority_score"], -t["answered"]))

        blocks: dict[str | None, dict] = {}
        for t in topics:
            b = blocks.setdefault(t["block"], {"block": t["block"], "answered": 0, "correct": 0})
            b["answered"] += t["answered"]
            b["correct"] += t["correct"]
        block_list = sorted(blocks.values(), key=lambda b: (b["block"] is None, str(b["block"] or "")))
        for b in block_list:
            b["accuracy"] = _pct(b["correct"], b["answered"])

        closed = self._session.execute(text(
            "SELECT DISTINCT s.id, s.started_at, s.final_score, s.question_ids FROM test_sessions s "
            "JOIN test_attempts a ON a.test_session_id = s.id "
            "JOIN question_syllabus_tags t ON t.question_id = a.question_id AND t.syllabus_id = :s "
            "WHERE s.final_score IS NOT NULL AND s.closed_at IS NOT NULL ORDER BY s.started_at"
        ), params).fetchall()
        evolution = [{"date": str(r.started_at)[:10], "score": float(r.final_score), "label": r.id} for r in closed]

        # Resultados de los tests terminados: lo contestado bien o mal y lo que quedó en blanco.
        answered_by_session = {
            r.test_session_id: (r.answered, r.correct) for r in self._session.execute(text(
                "SELECT test_session_id, COUNT(*) AS answered, COALESCE(SUM(is_correct), 0) AS correct "
                "FROM test_attempts WHERE selected_option_id IS NOT NULL GROUP BY test_session_id"
            ))
        }
        distribution = {"correct": 0, "wrong": 0, "blank": 0}
        for r in closed:
            answered, correct = answered_by_session.get(r.id, (0, 0))
            distribution["correct"] += correct
            distribution["wrong"] += answered - correct
            distribution["blank"] += max(len(json.loads(r.question_ids or "[]")) - answered, 0)

        return {
            "blocks": block_list,
            "distribution": distribution,
            "trend": trend([p["score"] for p in evolution], 5),
            "exams": self._exam_progress(syllabus_id),
            "recurrent": self._recurrent_mistakes(attempts_sql, params),
            "answered": totals.answered,
            "correct": totals.correct,
            "accuracy": _pct(totals.correct, totals.answered),
            "questions_seen": totals.questions,
            "pool": pool,
            "coverage": _pct(totals.questions, pool),
            "sessions": totals.sessions,
            "pending": pending,
            "topics": topics,
            "evolution": evolution,
        }
