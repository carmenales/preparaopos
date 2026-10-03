"""TestSessionService: Iniciar sesión, registrar respuestas, cerrar y calcular resultado."""

from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

from domain.scoring.models import ScoringRule
from domain.sessions.models import AnswerResult, QuestionResult, SessionResult, TestAttempt, TestSession


# Regla oficial AGE por defecto si no se indica otra en BD
DEFAULT_AGE_SCORING_RULE = ScoringRule(
    id=1,
    code="age-oficial-tercio",
    name="AGE oficial A - F/3",
    correct_score=Decimal("1"),
    wrong_penalty=Decimal("1") / Decimal("3"),
    blank_score=Decimal("0"),
    score_scale=Decimal("100"),
    min_score_zero=True,
    # TODO: confirmar regla de redondeo oficial de la convocatoria específica,
    # asumido ROUND_HALF_UP provisionalmente
    round_decimals=2,
    rounding_mode=ROUND_HALF_UP,
)


class TestSessionService:
    __test__ = False

    def __init__(
        self,
        session_repository,
        question_repository,
        scoring_service,
        exam_repository=None,
        scoring_rule_repository=None,
    ) -> None:
        self._sessions = session_repository
        self._questions = question_repository
        self._scoring = scoring_service
        self._exams = exam_repository
        self._scoring_rules = scoring_rule_repository

    def start_session(
        self,
        *,
        mode: Literal["practice", "exam"],
        source: Literal["block", "exam", "random"],
        source_ref: str | None = None,
        question_count: int | None = None,
        include_reserves: bool = False,
    ) -> TestSession:
        """Crea una nueva sesión con un conjunto inmutable de preguntas ordenadas."""
        duration_seconds: int | None = None
        scoring_rule_id: int | None = None
        exam_id: int | None = None
        question_ids: list[int] = []

        if source == "exam":
            if not source_ref:
                raise ValueError("source='exam' requiere source_ref con exam_id")
            exam_id = int(source_ref)
            if self._exams is None:
                raise RuntimeError("ExamRepository no configurado")
            exam = self._exams.get_by_id(exam_id)
            if exam is None:
                raise ValueError(f"Examen con id={exam_id} no encontrado")

            scoring_rule_id = exam.scoring_rule_id

            # Filtra preguntas: por defecto solo ordinarias válidas (is_reserve=False)
            exam_questions = [
                eq for eq in exam.questions
                if include_reserves or not eq.is_reserve
            ]
            exam_questions.sort(key=lambda eq: eq.position)
            question_ids = [eq.question_id for eq in exam_questions]

            if mode == "exam":
                duration_seconds = exam.duration_seconds
            else:
                duration_seconds = None

        elif source == "block":
            if not source_ref:
                raise ValueError("source='block' requiere source_ref (ej. 'syllabus_id:block' o 'block')")
            parts = source_ref.split(":")
            syllabus_id: str | None = None
            block: str | None = None
            topic: str | None = None

            if len(parts) == 1:
                block = parts[0]
            elif len(parts) == 2:
                syllabus_id, block = parts[0], parts[1]
            elif len(parts) >= 3:
                syllabus_id, block, topic = parts[0], parts[1], parts[2]

            questions = self._questions.list_by_filters(
                syllabus_id=syllabus_id,
                block=block,
                topic=topic,
            )
            q_ids = [q.id for q in questions]
            random.shuffle(q_ids)
            if question_count and question_count > 0:
                q_ids = q_ids[:question_count]
            question_ids = q_ids

        elif source == "random":
            questions = self._questions.list_by_filters()
            q_ids = [q.id for q in questions]
            random.shuffle(q_ids)
            count = question_count if (question_count and question_count > 0) else 30
            question_ids = q_ids[:count]

        else:
            raise ValueError(f"Fuente no soportada: {source}")

        session_id = uuid.uuid4().hex
        started_at = datetime.now(timezone.utc)

        session = TestSession(
            id=session_id,
            mode=mode,
            source=source,
            source_ref=source_ref,
            question_ids=question_ids,
            started_at=started_at,
            duration_seconds=duration_seconds,
            scoring_rule_id=scoring_rule_id,
            exam_id=exam_id,
            status="open",
        )

        self._sessions.save_session(session)
        return session

    def remaining_seconds(self, session_or_id: TestSession | str, now: datetime | None = None) -> int | None:
        """Autoridad de tiempo en servidor. None = sin límite de tiempo (práctica)."""
        session = (
            session_or_id
            if isinstance(session_or_id, TestSession)
            else self._sessions.get_by_id(session_or_id)
        )
        if session is None or session.duration_seconds is None:
            return None

        clock = now or datetime.now(timezone.utc)
        started = session.started_at
        if started.tzinfo is None:
            started = started.replace(tzinfo=timezone.utc)
        if clock.tzinfo is None:
            clock = clock.replace(tzinfo=timezone.utc)

        elapsed = (clock - started).total_seconds()
        remaining = int(session.duration_seconds - elapsed)
        return max(0, remaining)

    def is_expired(self, session_or_id: TestSession | str, now: datetime | None = None) -> bool:
        """Determina si la sesión ha agotado el tiempo oficial asignado."""
        remaining = self.remaining_seconds(session_or_id, now)
        return remaining is not None and remaining <= 0

    def submit_answer(
        self,
        *,
        session_id: str,
        question_id: int,
        selected_option_id: int | None,
        now: datetime | None = None,
    ) -> AnswerResult | None:
        """Registra o actualiza una respuesta (upsert).
        
        Si la sesión expiró o está cerrada, rechaza la respuesta.
        En modo 'practice', devuelve corrección inline. En 'exam', oculta el resultado.
        """
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")

        clock = now or datetime.now(timezone.utc)

        # 1. Comprobación de expiración de tiempo
        if self.is_expired(session, clock):
            self.close_session(session_id, now=clock)
            return None

        # 2. Comprobación de sesión ya cerrada
        if session.closed_at is not None or session.status == "closed":
            return None

        if question_id not in session.question_ids:
            raise ValueError(f"La pregunta {question_id} no pertenece a la sesión {session_id}")

        # 3. Determinar acierto para guardar en BD
        q_dto = self._questions.get_by_id(question_id)
        correct_option_id: int | None = None
        explanation: str | None = None
        is_correct: bool | None = None

        if q_dto:
            explanation = q_dto.justification
            for opt in q_dto.options:
                if opt.is_correct:
                    correct_option_id = opt.id
                    if not explanation and opt.justification:
                        explanation = opt.justification

            if selected_option_id is not None:
                is_correct = (selected_option_id == correct_option_id)

        attempt = TestAttempt(
            session_id=session_id,
            question_id=question_id,
            selected_option_id=selected_option_id,
            answered_at=clock,
            is_correct=is_correct,
        )
        self._sessions.save_attempt(attempt)

        # 4. Modo práctica vs examen
        if session.mode == "practice":
            return AnswerResult(
                session_id=session_id,
                question_id=question_id,
                selected_option_id=selected_option_id,
                is_saved=True,
                is_correct=is_correct,
                correct_option_id=correct_option_id,
                explanation=explanation,
            )
        else:
            return AnswerResult(
                session_id=session_id,
                question_id=question_id,
                selected_option_id=selected_option_id,
                is_saved=True,
                is_correct=None,
                correct_option_id=None,
                explanation=None,
            )

    def close_session(self, session_id: str, now: datetime | None = None) -> TestSession:
        """Cierra la sesión y calcula la calificación con ScoringService (idempotente)."""
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")

        if session.closed_at is not None:
            return session

        clock = now or datetime.now(timezone.utc)
        questions_map = self._questions.get_by_ids(session.question_ids)
        attempts_map = {att.question_id: att for att in session.attempts}

        correct_count = 0
        wrong_count = 0
        blank_count = 0
        annulled_count = 0

        for qid in session.question_ids:
            q = questions_map.get(qid)
            if q and q.is_annulled:
                annulled_count += 1
                continue

            att = attempts_map.get(qid)
            if att is None or att.selected_option_id is None:
                blank_count += 1
            elif att.is_correct:
                correct_count += 1
            else:
                wrong_count += 1

        rule = None
        if session.scoring_rule_id and self._scoring_rules:
            rule = self._scoring_rules.get_by_id(session.scoring_rule_id)
        if rule is None:
            rule = DEFAULT_AGE_SCORING_RULE

        final_score = self._scoring.score_scaled(
            correct=correct_count,
            wrong=wrong_count,
            blank=blank_count,
            annulled=annulled_count,
            total_questions=len(session.question_ids),
            rule=rule,
        )

        session.closed_at = clock
        session.status = "closed"
        session.final_score = final_score

        self._sessions.save_session(session)
        return session

    def get_result(self, session_id: str) -> SessionResult:
        """Devuelve la hoja de resultados completa con desglose por pregunta."""
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")

        if session.closed_at is None:
            session = self.close_session(session_id)

        questions_map = self._questions.get_by_ids(session.question_ids)
        attempts_map = {att.question_id: att for att in session.attempts}

        correct_count = 0
        wrong_count = 0
        blank_count = 0
        annulled_count = 0
        q_results: list[QuestionResult] = []

        for qid in session.question_ids:
            q = questions_map.get(qid)
            correct_opt_id: int | None = None
            explanation: str | None = None
            if q:
                explanation = q.justification
                for o in q.options:
                    if o.is_correct:
                        correct_opt_id = o.id
                        if not explanation and o.justification:
                            explanation = o.justification

            if q and q.is_annulled:
                annulled_count += 1
                q_results.append(
                    QuestionResult(
                        question_id=qid,
                        selected_option_id=None,
                        correct_option_id=correct_opt_id,
                        is_correct=None,
                        is_blank=False,
                        explanation=explanation,
                    )
                )
                continue

            att = attempts_map.get(qid)
            if att is None or att.selected_option_id is None:
                blank_count += 1
                q_results.append(
                    QuestionResult(
                        question_id=qid,
                        selected_option_id=None,
                        correct_option_id=correct_opt_id,
                        is_correct=None,
                        is_blank=True,
                        explanation=explanation,
                    )
                )
            elif att.is_correct:
                correct_count += 1
                q_results.append(
                    QuestionResult(
                        question_id=qid,
                        selected_option_id=att.selected_option_id,
                        correct_option_id=correct_opt_id,
                        is_correct=True,
                        is_blank=False,
                        explanation=explanation,
                    )
                )
            else:
                wrong_count += 1
                q_results.append(
                    QuestionResult(
                        question_id=qid,
                        selected_option_id=att.selected_option_id,
                        correct_option_id=correct_opt_id,
                        is_correct=False,
                        is_blank=False,
                        explanation=explanation,
                    )
                )

        evaluable = len(session.question_ids) - annulled_count

        return SessionResult(
            session_id=session.id,
            mode=session.mode,
            final_score=session.final_score,
            correct_count=correct_count,
            wrong_count=wrong_count,
            blank_count=blank_count,
            annulled_count=annulled_count,
            total_evaluable=evaluable,
            questions=q_results,
        )
