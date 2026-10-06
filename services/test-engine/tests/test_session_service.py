"""
Pruebas para TestSessionService según especificación:
1. test_start_session_exam_excludes_reserves_by_default
2. test_start_session_exam_respects_question_order
3. test_submit_answer_rejected_after_expiry
4. test_submit_answer_upsert_changes_previous_selection
5. test_close_session_is_idempotent
6. test_close_session_computes_score_via_scoring_service
7. test_practice_mode_reveals_correction_immediately
8. test_exam_mode_hides_correction_until_close
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import SQLITE_PATH
from domain.scoring.service import ScoringService
from domain.sessions.service import TestSessionService
from infrastructure.db.repositories.exam_repository import ExamRepository
from infrastructure.db.repositories.question_repository import QuestionRepository
from infrastructure.db.repositories.scoring_rule_repository import ScoringRuleRepository
from infrastructure.db.repositories.session_repository import SessionRepository


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(f"sqlite:///{SQLITE_PATH}")
    with Session(engine) as session:
        yield session


@pytest.fixture
def session_service(db_session: Session) -> TestSessionService:
    session_repo = SessionRepository(db_session)
    question_repo = QuestionRepository(db_session)
    exam_repo = ExamRepository(db_session)
    rule_repo = ScoringRuleRepository(db_session)
    scoring_service = ScoringService()
    return TestSessionService(
        session_repository=session_repo,
        question_repository=question_repo,
        scoring_service=scoring_service,
        exam_repository=exam_repo,
        scoring_rule_repository=rule_repo,
    )


def test_start_session_exam_excludes_reserves_by_default(session_service: TestSessionService):
    """1. Simulacro examen AGE GSI 2024 (exam_id=53): exactamente 96 preguntas ordinarias, 0 de reserva."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    assert session is not None
    assert len(session.question_ids) == 96
    # Comprobar que ninguna de las 5 preguntas de reserva está incluida
    # (IDs de reserva en 2024: 18108 a 18112)
    reserve_ids = {18108, 18109, 18110, 18111, 18112}
    for qid in session.question_ids:
        assert qid not in reserve_ids

    # Duración oficial asignada automáticamente en modo examen: 6000s (100 min)
    assert session.duration_seconds == 6000


def test_start_session_exam_respects_question_order(session_service: TestSessionService, db_session: Session):
    """2. Las preguntas de la sesión respetan estrictamente el orden de position en exam_questions."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    from infrastructure.db import orm_models as orm
    from sqlalchemy import select

    ordered_ordinary = db_session.scalars(
        select(orm.ExamQuestion.question_id)
        .where(orm.ExamQuestion.exam_id == 53, orm.ExamQuestion.is_reserve == False)
        .order_by(orm.ExamQuestion.position)
    ).all()

    assert session.question_ids == ordered_ordinary


def test_submit_answer_rejected_after_expiry(session_service: TestSessionService):
    """3. La respuesta es rechazada si se envía después de que haya expirado el tiempo oficial."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    qid = session.question_ids[0]

    # Simular tiempo después de expirar (6001 segundos después)
    start_time = session.started_at
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    after_expiry = start_time + timedelta(seconds=session.duration_seconds + 10)

    ans = session_service.submit_answer(
        session_id=session.id,
        question_id=qid,
        selected_option_id=1,
        now=after_expiry,
    )
    # Debe ser rechazado (None) y la sesión debe quedar cerrada
    assert ans is None
    closed = session_service._sessions.get_by_id(session.id)
    assert closed.closed_at is not None
    assert closed.status == "closed"


def test_submit_answer_upsert_changes_previous_selection(session_service: TestSessionService, db_session: Session):
    """4. Cambiar la opción seleccionada antes de cerrar actualiza el registro (upsert)."""
    session = session_service.start_session(
        mode="practice",
        source="exam",
        source_ref="53",
    )
    qid = session.question_ids[0]

    # Primera respuesta: opción 100
    res1 = session_service.submit_answer(
        session_id=session.id,
        question_id=qid,
        selected_option_id=100,
    )
    assert res1 is not None

    # Segunda respuesta en la misma pregunta: cambia a opción 200
    res2 = session_service.submit_answer(
        session_id=session.id,
        question_id=qid,
        selected_option_id=200,
    )
    assert res2 is not None

    # Verificar en BD que solo hay 1 attempt para esa (session, question) con selected_option_id=200
    from infrastructure.db import orm_models as orm
    from sqlalchemy import select

    attempts = db_session.scalars(
        select(orm.TestAttempt).where(
            orm.TestAttempt.test_session_id == session.id,
            orm.TestAttempt.question_id == qid,
        )
    ).all()
    assert len(attempts) == 1
    assert attempts[0].selected_option_id == 200


def test_close_session_is_idempotent(session_service: TestSessionService):
    """5. Cerrar la sesión dos veces es idempotente: no recalcula ni cambia closed_at."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    closed_1 = session_service.close_session(session.id)
    first_closed_at = closed_1.closed_at
    first_score = closed_1.final_score

    # Segundo cierre
    closed_2 = session_service.close_session(session.id)
    assert closed_2.closed_at == first_closed_at
    assert closed_2.final_score == first_score


def test_close_session_computes_score_via_scoring_service(session_service: TestSessionService):
    """6. close_session integra ScoringService real para calcular la nota final escalada."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    # Responder 60 aciertos en las primeras 60 preguntas:
    # Buscar para cada pregunta su opción correcta
    q_map = session_service._questions.get_by_ids(session.question_ids[:60])
    for qid in session.question_ids[:60]:
        q = q_map[qid]
        corr_opt = next(o for o in q.options if o.is_correct)
        session_service.submit_answer(
            session_id=session.id,
            question_id=qid,
            selected_option_id=corr_opt.id,
        )

    # Las 36 restantes se quedan en blanco
    closed = session_service.close_session(session.id)

    # 60 aciertos, 0 fallos, 36 blancos sobre 96 evaluables.
    # Regla: correct=1, wrong=1/3, blank=0, scale=10 (o 100).
    # Nota neta: 60. Escalado sobre 96 preguntas: (60 / 96) * score_scale
    assert closed.final_score is not None
    assert closed.final_score > 0
    # Si la regla en BD tiene score_scale=10: (60 / 96) * 10 = 6.25
    expected = (Decimal("60") / Decimal("96")) * Decimal("10")
    assert closed.final_score == expected.quantize(Decimal("0.01"))


def test_practice_mode_reveals_correction_immediately(session_service: TestSessionService):
    """7. En modo práctica, submit_answer devuelve de inmediato si acertó, la opción correcta y explicación."""
    session = session_service.start_session(
        mode="practice",
        source="exam",
        source_ref="53",
    )
    qid = session.question_ids[0]
    q = session_service._questions.get_by_id(qid)
    corr_opt = next(o for o in q.options if o.is_correct)

    ans = session_service.submit_answer(
        session_id=session.id,
        question_id=qid,
        selected_option_id=corr_opt.id,
    )
    assert ans is not None
    assert ans.is_correct is True
    assert ans.correct_option_id == corr_opt.id
    # Revela explicación si existe en la pregunta
    if q.justification:
        assert ans.explanation == q.justification


def test_exam_mode_hides_correction_until_close(session_service: TestSessionService):
    """8. En modo examen, submit_answer oculta corrección (None). get_result revela la corrección tras cerrar."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    qid = session.question_ids[0]
    q = session_service._questions.get_by_id(qid)
    corr_opt = next(o for o in q.options if o.is_correct)

    ans = session_service.submit_answer(
        session_id=session.id,
        question_id=qid,
        selected_option_id=corr_opt.id,
    )
    assert ans is not None
    # En modo examen, los datos de corrección NO se revelan durante el examen
    assert ans.is_correct is None
    assert ans.correct_option_id is None
    assert ans.explanation is None

    # Al cerrar y solicitar resultados, la corrección completa sí se revela
    result = session_service.get_result(session.id)
    assert result.session_id == session.id
    assert len(result.questions) == 96
    first_q_res = next(qr for qr in result.questions if qr.question_id == qid)
    assert first_q_res.is_correct is True
    assert first_q_res.correct_option_id == corr_opt.id


def test_close_session_counts_unattempted_questions_as_blank(session_service: TestSessionService):
    """9. Preguntas nunca abiertas (0 filas TestAttempt) se cuentan como blancos y se evalúan sobre las 96 totales."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    # El opositor responde 30 preguntas de 96 (20 aciertos, 10 fallos):
    q_map = session_service._questions.get_by_ids(session.question_ids[:30])
    for i, qid in enumerate(session.question_ids[:30]):
        q = q_map[qid]
        corr_opt = next(o for o in q.options if o.is_correct)
        wrong_opt = next(o for o in q.options if not o.is_correct)

        chosen = corr_opt.id if i < 20 else wrong_opt.id
        session_service.submit_answer(
            session_id=session.id,
            question_id=qid,
            selected_option_id=chosen,
        )

    # Las 66 preguntas restantes NUNCA fueron respondidas (sin fila TestAttempt)
    closed = session_service.close_session(session.id)
    res = session_service.get_result(session.id)

    assert res.correct_count == 20
    assert res.wrong_count == 10
    assert res.blank_count == 66  # 96 - 30 = 66 en blanco
    assert res.total_evaluable == 96

    # Nota: (20 - 10/3) / 96 * 10 = (16.6666... / 96) * 10 = 1.7361... -> 1.74
    expected = (Decimal("20") - Decimal("10") / Decimal("3")) / Decimal("96") * Decimal("10")
    assert closed.final_score == expected.quantize(Decimal("0.01"))
    assert res.final_score == closed.final_score

    # Verificar que exactamente 66 QuestionResult tienen is_blank=True y selected_option_id=None
    blanks = [qr for qr in res.questions if qr.is_blank]
    assert len(blanks) == 66
    for b in blanks:
        assert b.selected_option_id is None
        assert b.is_correct is None


def test_abandoned_expired_session_is_lazily_closed(session_service: TestSessionService):
    """10. Sesión abandonada tras expirar: al consultarse (get_session o get_result) se cierra de forma perezosa."""
    session = session_service.start_session(
        mode="exam",
        source="exam",
        source_ref="53",
    )
    # Sesión abierta inicialmente
    assert session.closed_at is None
    assert session.status == "open"

    # Simular que el usuario cierra la pestaña y 2 horas después (7200s > 6000s) consulta su sesión
    start_time = session.started_at
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    future_time = start_time + timedelta(seconds=7200)

    # get_session debe detectar la expiración y cerrarla automáticamente
    lazy_closed = session_service.get_session(session.id, now=future_time)
    assert lazy_closed is not None
    assert lazy_closed.closed_at is not None
    assert lazy_closed.status == "closed"
    # El closed_at queda fijado a la expiración exacta (started + 6000s)
    expected_expiry = start_time + timedelta(seconds=6000)
    assert lazy_closed.closed_at == expected_expiry
    # Al no responder ninguna pregunta, las 96 son blancos -> nota 0.00
    assert lazy_closed.final_score == Decimal("0.00")
