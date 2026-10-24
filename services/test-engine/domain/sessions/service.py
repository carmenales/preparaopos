"""TestSessionService: Iniciar sesión, registrar respuestas, cerrar y calcular resultado."""

from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

from domain.scoring.models import ScoringRule
from domain.sessions.generator import (
    SECONDS_PER_QUESTION,
    GeneratorFilters,
    NoQuestionsForFilters,
    question_weights,
    weighted_sample,
)
from domain.sessions.models import (
    AnswerResult,
    LiveSummary,
    QuestionResult,
    SessionResult,
    TestAttempt,
    TestSession,
)


# Regla oficial AGE por defecto si no se indica otra en BD
DEFAULT_AGE_SCORING_RULE = ScoringRule(
    id=1,
    code="age-oficial-tercio",
    name="AGE oficial A - F/3",
    correct_score=Decimal("1"),
    wrong_penalty=Decimal("1") / Decimal("3"),
    blank_score=Decimal("0"),
    score_scale=Decimal("10"),  # la hoja de resultados muestra la nota sobre 10
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
        source: Literal["block", "exam", "random", "questions", "note", "generated"],
        source_ref: str | None = None,
        question_count: int | None = None,
        include_reserves: bool = False,
        explicit_question_ids: list[int] | None = None,
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

        elif source == "generated":
            filters = GeneratorFilters.from_source_ref(source_ref or "")
            if filters.weighted:
                tagged = self._questions.list_tagged_for_generator(filters)
                if not tagged:
                    raise NoQuestionsForFilters("Ninguna pregunta cumple los filtros elegidos")
                weights = question_weights(tagged, self._questions.topic_frequencies(filters.syllabus_id))
                question_ids = weighted_sample(weights, filters.count)
            else:
                q_ids = self._questions.list_ids_for_generator(filters)
                if not q_ids:
                    raise NoQuestionsForFilters("Ninguna pregunta cumple los filtros elegidos")
                random.shuffle(q_ids)
                question_ids = q_ids[: filters.count]
            source_ref = filters.to_source_ref()
            if self._exams is not None:
                scoring_rule_id = self._exams.single_scoring_rule_for_syllabus(filters.syllabus_id)
            if mode == "exam":
                duration_seconds = len(question_ids) * SECONDS_PER_QUESTION

        elif source == "random":
            questions = self._questions.list_by_filters()
            q_ids = [q.id for q in questions]
            random.shuffle(q_ids)
            count = question_count if (question_count and question_count > 0) else 30
            question_ids = q_ids[:count]

        elif source == "questions":
            if explicit_question_ids:
                question_ids = [int(x) for x in explicit_question_ids]
            elif not source_ref:
                raise ValueError("source='questions' requiere source_ref con IDs de preguntas separados por comas")
            else:
                try:
                    question_ids = [int(x.strip()) for x in source_ref.split(",") if x.strip()]
                except ValueError:
                    raise ValueError("source_ref contiene IDs de preguntas no válidos")
            if not question_ids:
                raise ValueError("No se encontraron preguntas válidas")

        elif source == "note":
            if explicit_question_ids:
                question_ids = [int(x) for x in explicit_question_ids]
            elif source_ref and "," in source_ref:
                question_ids = [int(x.strip()) for x in source_ref.split(",") if x.strip()]
            else:
                question_ids = []
            if not question_ids:
                raise ValueError(f"No se encontraron preguntas válidas para el apunte '{source_ref}'")

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

    # ------------------------------------------------------------------
    # Cronómetro pausable (como PreparaTIC): el tiempo es el que ha corrido
    # el cronómetro, no el transcurrido desde que se creó el test. Al llegar
    # al límite no se cierra nada: decide el usuario («Un poquito más» o
    # «Corregir»).
    # ------------------------------------------------------------------

    @staticmethod
    def time_limit(session: TestSession) -> int:
        """Tiempo del test: el del examen o, si no tiene, 1 minuto por pregunta."""
        return session.duration_seconds or len(session.question_ids) * SECONDS_PER_QUESTION

    @staticmethod
    def elapsed_seconds(session: TestSession, now: datetime | None = None) -> int:
        elapsed = session.timer_elapsed_seconds or 0
        if session.timer_running_since is not None:
            clock = now or datetime.now(timezone.utc)
            since = session.timer_running_since
            if since.tzinfo is None:
                since = since.replace(tzinfo=timezone.utc)
            elapsed += max(0, int((clock - since).total_seconds()))
        return elapsed

    def timer_state(self, session: TestSession, now: datetime | None = None) -> dict:
        return {"limit": self.time_limit(session), "elapsed": self.elapsed_seconds(session, now),
                "running": session.timer_running_since is not None,
                "started": session.timer_elapsed_seconds is not None}

    def remaining_seconds(self, session_or_id: TestSession | str, now: datetime | None = None) -> int | None:
        """Lo que le queda al cronómetro (0 si se ha pasado del límite)."""
        session = (session_or_id if isinstance(session_or_id, TestSession)
                   else self._sessions.get_by_id(session_or_id))
        if session is None:
            return None
        return max(0, self.time_limit(session) - self.elapsed_seconds(session, now))

    def timer_action(self, session_id: str, action: str, now: datetime | None = None) -> TestSession:
        """start | pause | reset. Con el test cerrado no cambia nada."""
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")
        if session.closed_at is not None:
            return session
        clock = now or datetime.now(timezone.utc)
        if action == "start":
            if session.timer_running_since is None:
                session.timer_elapsed_seconds = session.timer_elapsed_seconds or 0
                session.timer_running_since = clock
        elif action == "pause":
            session.timer_elapsed_seconds = self.elapsed_seconds(session, clock)
            session.timer_running_since = None
        elif action == "reset":
            session.timer_elapsed_seconds = 0
            session.timer_running_since = None
        else:
            raise ValueError(f"Acción de cronómetro desconocida: {action}")
        self._sessions.save_session(session)
        return session

    def submit_answer(
        self,
        *,
        session_id: str,
        question_id: int,
        selected_option_id: int | None,
        now: datetime | None = None,
    ) -> AnswerResult | None:
        """Registra o actualiza una respuesta (upsert). ``selected_option_id=None`` la borra:
        la pregunta vuelve a estar sin contestar (cuenta como blanco al corregir).

        Si la sesión expiró o está cerrada, rechaza la respuesta.
        Si el test corrige al responder (``feedback_now``), devuelve la corrección; si no, la oculta.
        """
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")

        clock = now or datetime.now(timezone.utc)

        # Con el test ya corregido no se admiten respuestas. El tiempo no cierra el test:
        # al acabarse, el usuario decide si sigue («Un poquito más») o corrige.
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

        if selected_option_id is None:
            # Sin respuesta no se guarda fila: así no cuenta como respondida en ninguna estadística.
            self._sessions.delete_attempt(session_id, question_id)
        else:
            self._sessions.save_attempt(TestAttempt(
                session_id=session_id,
                question_id=question_id,
                selected_option_id=selected_option_id,
                answered_at=clock,
                is_correct=is_correct,
            ))

        # 4. Corrección al responder o al final
        if session.feedback_now:
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

    def answer_or_clear(self, *, session_id: str, question_id: int, option_id: int | None,
                        now: datetime | None = None) -> AnswerResult | None:
        """Pulsar una opción en la pantalla del test: la marca o, si ya era la marcada, la desmarca.

        Con corrección al responder, una pregunta ya contestada queda fijada (ya se ha visto si
        estaba bien): no se cambia ni se borra. Devuelve None si la sesión está cerrada o expiró.
        """
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")
        current = next((a for a in session.attempts if a.question_id == question_id), None)
        if session.feedback_now and current is not None and current.selected_option_id is not None:
            return AnswerResult(session_id=session_id, question_id=question_id,
                                selected_option_id=current.selected_option_id, is_saved=False,
                                is_correct=current.is_correct)
        if current is not None and option_id is not None and current.selected_option_id == option_id:
            option_id = None
        return self.submit_answer(session_id=session_id, question_id=question_id,
                                  selected_option_id=option_id, now=now)

    def set_feedback_mode(self, session_id: str, instant: bool) -> TestSession:
        """Cambia entre corregir al responder y corregir al final, también a mitad del test."""
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")
        session.instant_feedback = instant
        self._sessions.save_session(session)
        return session

    def _rule_for(self, session: TestSession) -> ScoringRule:
        rule = None
        if session.scoring_rule_id and self._scoring_rules:
            rule = self._scoring_rules.get_by_id(session.scoring_rule_id)
        return rule or DEFAULT_AGE_SCORING_RULE

    def live_summary(self, session: TestSession, questions_map: dict | None = None) -> LiveSummary:
        """Contestadas, aciertos, fallos y la nota si se corrigiera ahora (el resto, en blanco)."""
        questions_map = questions_map if questions_map is not None else self._questions.get_by_ids(session.question_ids)
        attempts = {a.question_id: a for a in session.attempts if a.selected_option_id is not None}
        correct = wrong = blank = annulled = 0
        for qid in session.question_ids:
            q = questions_map.get(qid)
            if q and q.is_annulled:
                annulled += 1
            elif qid not in attempts:
                blank += 1
            elif attempts[qid].is_correct:
                correct += 1
            else:
                wrong += 1
        score = self._scoring.score_scaled(correct=correct, wrong=wrong, blank=blank, annulled=annulled,
                                           total_questions=len(session.question_ids), rule=self._rule_for(session))
        return LiveSummary(total=len(session.question_ids), answered=correct + wrong, correct=correct,
                           wrong=wrong, blank=blank, annulled=annulled, estimated_score=score)

    def get_session(self, session_id: str, now: datetime | None = None) -> TestSession | None:
        return self._sessions.get_by_id(session_id)

    def list_sessions(self, limit: int = 50, now: datetime | None = None) -> list[TestSession]:
        return self._sessions.list_all(limit=limit)

    def close_session(self, session_id: str, now: datetime | None = None) -> TestSession:
        """Cierra la sesión y calcula la calificación con ScoringService (idempotente)."""
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")

        if session.closed_at is not None:
            return session

        clock = now or datetime.now(timezone.utc)
        if clock.tzinfo is None:
            clock = clock.replace(tzinfo=timezone.utc)

        # Se para el cronómetro: queda el tiempo empleado.
        if session.timer_running_since is not None:
            session.timer_elapsed_seconds = self.elapsed_seconds(session, clock)
            session.timer_running_since = None

        questions_map = self._questions.get_by_ids(session.question_ids)
        attempts_map = {att.question_id: att for att in session.attempts}

        correct_count = 0
        wrong_count = 0
        blank_count = 0
        annulled_count = 0

        for qid in session.question_ids:
            q = questions_map.get(qid)
            # NOTE: Para el examen 53 (AGE GSI 2024), ninguna pregunta tiene is_annulled=True:
            # las 4 anuladas del tribunal (posiciones 17, 27, 86, 90) NO se importaron como filas
            # en `questions` — se registraron solo en `scripts/etl/age_gsi_2024_anuladas.json`.
            # Este bloque existe para fuentes futuras donde sí se importen preguntas anuladas
            # con flag explícito (ej. bancos históricos donde la anulación ocurrió tras el import).
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

        rule = self._rule_for(session)

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

    def get_result(self, session_id: str, now: datetime | None = None) -> SessionResult:
        """Devuelve la hoja de resultados completa con desglose por pregunta."""
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Sesión {session_id} no encontrada")

        clock = now or datetime.now(timezone.utc)
        if session.closed_at is None:
            session = self.close_session(session_id, now=clock)

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
