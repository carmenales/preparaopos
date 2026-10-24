"""Repositorio de preguntas (SQLAlchemy)."""

from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload

from domain.questions.models import Option, Question as QuestionDTO, SyllabusTag
from infrastructure.db import orm_models as orm


class QuestionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_filters(
        self,
        *,
        syllabus_id: str | None = None,
        block: str | None = None,
        topic: str | None = None,
        exam_id: int | None = None,
        is_reserve: bool | None = None,
        pending_classification: bool | None = None,
    ) -> list[QuestionDTO]:
        stmt = select(orm.Question).options(
            selectinload(orm.Question.options),
            selectinload(orm.Question.tags),
        )

        if pending_classification is not None:
            stmt = stmt.where(orm.Question.pending_classification == pending_classification)

        if exam_id is not None:
            stmt = stmt.join(orm.ExamQuestion, orm.ExamQuestion.question_id == orm.Question.id).where(
                orm.ExamQuestion.exam_id == exam_id
            )
            if is_reserve is not None:
                stmt = stmt.where(orm.ExamQuestion.is_reserve == is_reserve)
            stmt = stmt.order_by(orm.ExamQuestion.position)

        if syllabus_id or block or topic:
            stmt = stmt.join(orm.QuestionSyllabusTag)
            if syllabus_id:
                stmt = stmt.where(orm.QuestionSyllabusTag.syllabus_id == syllabus_id)
            if block:
                stmt = stmt.where(orm.QuestionSyllabusTag.block == block)
            if topic:
                stmt = stmt.where(orm.QuestionSyllabusTag.topic == topic)

        rows = self._session.scalars(stmt).unique().all()
        return [self._to_domain(row) for row in rows]

    # ------------------------------------------------------------------
    # Generador de tests
    # ------------------------------------------------------------------

    # Pregunta fallada = su último intento respondido fue incorrecto (si después
    # se acierta, sale del refuerzo). Los intentos en blanco no cuentan.
    _FAILED_SQL = """
        SELECT a.question_id FROM test_attempts a
        WHERE a.selected_option_id IS NOT NULL
          AND a.is_correct = 0
          AND a.answered_at = (
              SELECT MAX(b.answered_at) FROM test_attempts b
              WHERE b.question_id = a.question_id AND b.selected_option_id IS NOT NULL
          )
    """

    def _generator_where(self, filters) -> tuple[str, dict]:
        clauses = ["t.syllabus_id = :syllabus_id", "q.is_annulled = 0"]
        params: dict = {"syllabus_id": filters.syllabus_id}
        if filters.block:
            clauses.append("t.block = :block")
            params["block"] = filters.block
        if filters.topic:
            clauses.append("t.topic = :topic")
            params["topic"] = filters.topic
        if filters.year is not None:
            clauses.append("q.year = :year")
            params["year"] = filters.year
        if filters.official_only:
            clauses.append("q.is_official_exam = 1")
        if filters.failed_only:
            clauses.append(f"q.id IN ({self._FAILED_SQL})")
        return " AND ".join(clauses), params

    def list_ids_for_generator(self, filters) -> list[int]:
        """Ids (sin repetir y ordenados) de las preguntas que cumplen los filtros del generador."""
        where, params = self._generator_where(filters)
        rows = self._session.execute(
            text(
                "SELECT DISTINCT q.id FROM questions q "
                "JOIN question_syllabus_tags t ON t.question_id = q.id "
                f"WHERE {where} ORDER BY q.id"
            ),
            params,
        )
        return [row[0] for row in rows]

    def list_tagged_for_generator(self, filters) -> list[tuple[int, str | None, str | None]]:
        """(id, bloque, tema) de las preguntas que cumplen los filtros, con su etiqueta en el temario."""
        where, params = self._generator_where(filters)
        rows = self._session.execute(
            text(
                "SELECT DISTINCT q.id, t.block, t.topic FROM questions q "
                "JOIN question_syllabus_tags t ON t.question_id = q.id "
                f"WHERE {where} ORDER BY q.id"
            ),
            params,
        )
        return [(r[0], r[1], r[2]) for r in rows]

    def topic_frequencies(self, syllabus_id: str) -> dict[tuple[str | None, str | None], int]:
        """Preguntas de examen oficial (no anuladas) por (bloque, tema) del temario: frecuencia histórica."""
        rows = self._session.execute(text(
            "SELECT t.block, t.topic, COUNT(DISTINCT q.id) FROM questions q "
            "JOIN question_syllabus_tags t ON t.question_id = q.id "
            "WHERE t.syllabus_id = :s AND q.is_annulled = 0 AND q.is_official_exam = 1 "
            "AND t.topic IS NOT NULL AND t.topic != '' GROUP BY t.block, t.topic"
        ), {"s": syllabus_id})
        return {(r[0], r[1]): int(r[2]) for r in rows}

    def count_for_generator(self, filters) -> int:
        where, params = self._generator_where(filters)
        return int(self._session.execute(
            text(
                "SELECT COUNT(DISTINCT q.id) FROM questions q "
                "JOIN question_syllabus_tags t ON t.question_id = q.id "
                f"WHERE {where}"
            ),
            params,
        ).scalar() or 0)

    def list_syllabi_with_counts(self) -> list[dict]:
        rows = self._session.execute(text(
            "SELECT s.id, s.name, s.organism, COUNT(DISTINCT q.id) AS n "
            "FROM syllabi s JOIN question_syllabus_tags t ON t.syllabus_id = s.id "
            "JOIN questions q ON q.id = t.question_id AND q.is_annulled = 0 "
            "GROUP BY s.id ORDER BY s.organism, s.name"
        ))
        return [{"id": r.id, "name": r.name, "organism": r.organism, "count": r.n} for r in rows]

    def generator_facets(self, syllabus_id: str, filters=None) -> dict:
        """Bloques, temas, años, oficiales y falladas de un temario, con su número de preguntas.

        Cada número tiene en cuenta los demás filtros elegidos en ``filters`` (pero no el suyo):
        con el bloque B3 · tema 107 elegido, cada año muestra las preguntas de ese tema en ese año,
        y «solo oficiales», las oficiales de ese tema y ese año. Así cuadran con el recuento final.
        """
        from dataclasses import replace

        from domain.sessions.generator import GeneratorFilters

        f = filters if filters is not None and filters.syllabus_id == syllabus_id else GeneratorFilters(syllabus_id)
        join = "FROM questions q JOIN question_syllabus_tags t ON t.question_id = q.id"

        def rows(sql_select: str, facet_filters, extra: str = "", tail: str = ""):
            where, params = self._generator_where(facet_filters)
            return self._session.execute(text(f"SELECT {sql_select} {join} WHERE {where}{extra} {tail}"), params)

        no_scope = replace(f, block=None, topic=None)
        topic_rows = rows("t.block, t.topic, COUNT(DISTINCT q.id) AS n", no_scope, " AND t.block IS NOT NULL",
                          "GROUP BY t.block, t.topic").fetchall()
        block_rows = rows("t.block, COUNT(DISTINCT q.id) AS n", no_scope, " AND t.block IS NOT NULL",
                          "GROUP BY t.block").fetchall()
        year_rows = rows("q.year, COUNT(DISTINCT q.id) AS n", replace(f, year=None), " AND q.year IS NOT NULL",
                         "GROUP BY q.year ORDER BY q.year DESC").fetchall()
        official = rows("COUNT(DISTINCT q.id)", replace(f, official_only=True)).scalar() or 0
        failed = rows("COUNT(DISTINCT q.id)", replace(f, failed_only=True)).scalar() or 0
        # La base del ponderado es la historia de todo el temario, no la de los filtros elegidos.
        weighted = self._session.execute(text(
            f"SELECT COUNT(DISTINCT q.id), COUNT(DISTINCT t.block || '|' || t.topic), MIN(q.year), MAX(q.year) "
            f"{join} WHERE t.syllabus_id = :s AND q.is_annulled = 0 "
            "AND q.is_official_exam = 1 AND t.topic IS NOT NULL AND t.topic != ''"
        ), {"s": syllabus_id}).first()

        def _num(value):
            return (0, int(value), "") if value and str(value).isdigit() else (1, 0, str(value or ""))

        topics_by_block: dict[str, list[dict]] = {}
        for r in topic_rows:
            if r.topic is not None:
                topics_by_block.setdefault(r.block, []).append({"topic": r.topic, "count": r.n})
        block_counts = {r.block: r.n for r in block_rows}
        years = [{"year": r.year, "count": r.n} for r in year_rows]
        # Lo elegido aparece aunque con los demás filtros se quede en 0 (la consulta no lo devuelve):
        # si no, desaparecería del desplegable y se perdería la selección.
        if f.block:
            block_counts.setdefault(f.block, 0)
            if f.topic and not any(t["topic"] == f.topic for t in topics_by_block.get(f.block, [])):
                topics_by_block.setdefault(f.block, []).append({"topic": f.topic, "count": 0})
        if f.year is not None and not any(y["year"] == f.year for y in years):
            years = sorted(years + [{"year": f.year, "count": 0}], key=lambda y: y["year"], reverse=True)
        blocks = []
        for block in sorted(block_counts, key=_num):
            topics = sorted(topics_by_block.get(block, []), key=lambda t: _num(t["topic"]))
            blocks.append({"block": block, "count": block_counts[block], "topics": topics})
        return {
            "blocks": blocks,
            "years": years,
            "official": int(official),
            "failed": int(failed),
            # Base del test ponderado: preguntas oficiales con tema. None si el temario no tiene.
            "weighted": ({"questions": int(weighted[0]), "topics": int(weighted[1]),
                          "year_from": weighted[2], "year_to": weighted[3]} if weighted and weighted[0] else None),
        }

    def get_by_id(self, question_id: int) -> QuestionDTO | None:
        stmt = (
            select(orm.Question)
            .options(
                selectinload(orm.Question.options),
                selectinload(orm.Question.tags),
            )
            .where(orm.Question.id == question_id)
        )
        row = self._session.scalar(stmt)
        return self._to_domain(row) if row else None

    def get_by_ids(self, question_ids: list[int]) -> dict[int, QuestionDTO]:
        if not question_ids:
            return {}
        stmt = (
            select(orm.Question)
            .options(
                selectinload(orm.Question.options),
                selectinload(orm.Question.tags),
            )
            .where(orm.Question.id.in_(question_ids))
        )
        rows = self._session.scalars(stmt).unique().all()
        return {row.id: self._to_domain(row) for row in rows}

    def count(self) -> int:
        from sqlalchemy import func

        return int(self._session.scalar(select(func.count()).select_from(orm.Question)) or 0)

    @staticmethod
    def _to_domain(row: orm.Question) -> QuestionDTO:
        return QuestionDTO(
            id=row.id,
            statement=row.statement,
            source=row.source,
            source_id=row.source_id,
            justification=row.justification,
            img_path=row.img_path,
            is_annulled=row.is_annulled,
            annulment_reason=row.annulment_reason,
            pending_classification=row.pending_classification,
            options=[
                Option(
                    id=opt.id,
                    text=opt.option_text,
                    is_correct=opt.is_correct,
                    display_order=opt.display_order,
                    justification=opt.justification,
                )
                for opt in row.options
            ],
            tags=[
                SyllabusTag(
                    syllabus_id=tag.syllabus_id,
                    block=tag.block,
                    topic=tag.topic,
                )
                for tag in row.tags
            ],
        )
