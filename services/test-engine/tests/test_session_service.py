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
from sqlalchemy import create_engine, text
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


def test_time_running_out_does_not_close_the_test(session_service: TestSessionService):
    """3. Con el cronómetro pausable, acabarse el tiempo no cierra el test: decide el usuario
    («Un poquito más» o «Corregir»). Solo se rechazan respuestas cuando ya está corregido."""
    session = session_service.start_session(mode="exam", source="exam", source_ref="53")
    qid = session.question_ids[0]
    opt = session_service._questions.get_by_id(qid).options[0].id
    after_limit = session.started_at + timedelta(seconds=session.duration_seconds + 10)

    ans = session_service.submit_answer(session_id=session.id, question_id=qid, selected_option_id=opt,
                                        now=after_limit)
    assert ans is not None
    assert session_service.get_session(session.id, now=after_limit).closed_at is None
    session_service.close_session(session.id)
    assert session_service.submit_answer(session_id=session.id, question_id=qid, selected_option_id=opt) is None


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


def test_pausable_timer_counts_only_running_time(session_service: TestSessionService):
    """10. El cronómetro acumula solo el tiempo en marcha; al corregir se congela el tiempo empleado."""
    session = session_service.start_session(mode="exam", source="exam", source_ref="53")
    t0 = datetime(2026, 10, 24, 10, 0, tzinfo=timezone.utc)
    state = session_service.timer_state(session)
    assert state == {"limit": 6000, "elapsed": 0, "running": False, "started": False}

    session_service.timer_action(session.id, "start", now=t0)
    session_service.timer_action(session.id, "pause", now=t0 + timedelta(seconds=600))
    paused = session_service.get_session(session.id)
    # Dos horas de pausa no cuentan
    assert session_service.elapsed_seconds(paused, now=t0 + timedelta(hours=2)) == 600
    assert session_service.remaining_seconds(paused, now=t0 + timedelta(hours=2)) == 5400

    session_service.timer_action(session.id, "start", now=t0 + timedelta(hours=2))
    running = session_service.get_session(session.id)
    assert session_service.elapsed_seconds(running, now=t0 + timedelta(hours=2, seconds=30)) == 630
    session_service.timer_action(session.id, "start", now=t0 + timedelta(hours=3))  # ya en marcha: no cambia
    assert session_service.get_session(session.id).timer_running_since == running.timer_running_since

    closed = session_service.close_session(session.id, now=t0 + timedelta(hours=2, seconds=90))
    assert closed.timer_running_since is None and closed.timer_elapsed_seconds == 690
    assert closed.final_score == Decimal("0.00")
    session_service.timer_action(session.id, "reset")  # con el test corregido no cambia nada
    assert session_service.get_session(session.id).timer_elapsed_seconds == 690

    other = session_service.start_session(mode="practice", source="exam", source_ref="53")
    session_service.timer_action(other.id, "start", now=t0)
    reset = session_service.timer_action(other.id, "reset", now=t0 + timedelta(seconds=50))
    assert (reset.timer_elapsed_seconds, reset.timer_running_since) == (0, None)


def test_session_without_scoring_rule_is_scored_out_of_ten(session_service: TestSessionService, db_session: Session):
    """Sin regla propia se usa la regla por defecto, y la nota es sobre 10 como muestra la hoja de resultados."""
    from sqlalchemy import text

    qid, correct_option = db_session.execute(text(
        "SELECT question_id, id FROM question_options WHERE is_correct = 1 ORDER BY id LIMIT 1"
    )).one()
    session = session_service.start_session(mode="practice", source="questions", source_ref=str(qid))
    assert session.scoring_rule_id is None
    session_service.submit_answer(session_id=session.id, question_id=qid, selected_option_id=correct_option)
    closed = session_service.close_session(session.id)
    assert closed.final_score == Decimal("10.00")


# --- Pantalla del test: desmarcar, corregir al responder o al final, marcador en vivo ---

def _exam_session(session_service, mode="exam"):
    return session_service.start_session(mode=mode, source="exam", source_ref="53")


def test_clicking_the_selected_option_again_leaves_it_blank_without_a_row(session_service, db_session):
    s = _exam_session(session_service)
    qid = s.question_ids[0]
    opt = session_service._questions.get_by_id(qid).options[0].id
    session_service.answer_or_clear(session_id=s.id, question_id=qid, option_id=opt)
    assert db_session.execute(text("SELECT COUNT(*) FROM test_attempts WHERE test_session_id = :s"),
                              {"s": s.id}).scalar() == 1
    session_service.answer_or_clear(session_id=s.id, question_id=qid, option_id=opt)
    db_session.expire_all()
    assert db_session.execute(text("SELECT COUNT(*) FROM test_attempts WHERE test_session_id = :s"),
                              {"s": s.id}).scalar() == 0
    assert session_service.get_result(s.id).blank_count == len(s.question_ids)


def test_instant_feedback_locks_answered_questions(session_service):
    s = _exam_session(session_service, mode="practice")
    qid = s.question_ids[0]
    options = session_service._questions.get_by_id(qid).options
    first = session_service.answer_or_clear(session_id=s.id, question_id=qid, option_id=options[0].id)
    assert first.correct_option_id is not None
    again = session_service.answer_or_clear(session_id=s.id, question_id=qid, option_id=options[1].id)
    assert again.is_saved is False and again.selected_option_id == options[0].id
    cleared = session_service.answer_or_clear(session_id=s.id, question_id=qid, option_id=None)
    assert cleared.is_saved is False


def test_feedback_mode_switch_mid_test(session_service):
    s = _exam_session(session_service)
    assert s.feedback_now is False
    qid = s.question_ids[0]
    opt = session_service._questions.get_by_id(qid).options[0].id
    assert session_service.submit_answer(session_id=s.id, question_id=qid, selected_option_id=opt).correct_option_id is None
    session_service.set_feedback_mode(s.id, True)
    assert session_service.get_session(s.id).feedback_now is True
    assert session_service.submit_answer(session_id=s.id, question_id=qid, selected_option_id=opt).correct_option_id is not None


def test_live_summary_scores_as_if_the_rest_were_blank(session_service):
    s = _exam_session(session_service, mode="practice")
    for qid in s.question_ids[:3]:
        q = session_service._questions.get_by_id(qid)
        session_service.answer_or_clear(session_id=s.id, question_id=qid, option_id=next(o.id for o in q.options if o.is_correct))
    q = session_service._questions.get_by_id(s.question_ids[3])
    session_service.answer_or_clear(session_id=s.id, question_id=s.question_ids[3],
                                    option_id=next(o.id for o in q.options if not o.is_correct))
    live = session_service.live_summary(session_service.get_session(s.id))
    assert (live.answered, live.correct, live.wrong) == (4, 3, 1)
    assert live.blank == len(s.question_ids) - 4 - live.annulled
    closed = session_service.close_session(s.id)
    assert live.estimated_score == closed.final_score
