"""Tablas SQLAlchemy del banco unificado (SQLite)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Syllabus(Base):
    __tablename__ = "syllabi"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    organism: Mapped[str] = mapped_column(String(64), nullable=False)

    tags: Mapped[list[QuestionSyllabusTag]] = relationship(back_populates="syllabus")
    exams: Mapped[list[Exam]] = relationship(back_populates="syllabus")


class ScoringRule(Base):
    __tablename__ = "scoring_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    correct_score: Mapped[Decimal] = mapped_column(Numeric(12, 6), nullable=False)
    wrong_penalty: Mapped[Decimal] = mapped_column(Numeric(12, 6), nullable=False)
    blank_score: Mapped[Decimal] = mapped_column(Numeric(12, 6), nullable=False, default=0)
    score_scale: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False, default=10)
    min_score_zero: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (UniqueConstraint("source", "source_id", name="uq_questions_source_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    justification: Mapped[str | None] = mapped_column(Text, nullable=True)
    img_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    is_annulled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    annulment_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    pending_classification: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    options: Mapped[list[QuestionOption]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.display_order",
    )
    tags: Mapped[list[QuestionSyllabusTag]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )


class QuestionOption(Base):
    __tablename__ = "question_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    justification: Mapped[str | None] = mapped_column(Text, nullable=True)

    question: Mapped[Question] = relationship(back_populates="options")


class QuestionSyllabusTag(Base):
    __tablename__ = "question_syllabus_tags"
    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "syllabus_id",
            "block",
            "topic",
            name="uq_question_syllabus_tag",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    syllabus_id: Mapped[str] = mapped_column(
        ForeignKey("syllabi.id"),
        nullable=False,
        index=True,
    )
    block: Mapped[str | None] = mapped_column(String(32), nullable=True)
    topic: Mapped[str | None] = mapped_column(String(32), nullable=True)

    question: Mapped[Question] = relationship(back_populates="tags")
    syllabus: Mapped[Syllabus] = relationship(back_populates="tags")


class Exam(Base):
    __tablename__ = "exams"
    __table_args__ = (UniqueConstraint("name", "syllabus_id", name="uq_exam_name_syllabus"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    convocatoria: Mapped[str | None] = mapped_column(String(128), nullable=True)
    syllabus_id: Mapped[str | None] = mapped_column(ForeignKey("syllabi.id"), nullable=True)
    scoring_rule_id: Mapped[int | None] = mapped_column(
        ForeignKey("scoring_rules.id"),
        nullable=True,
    )
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    syllabus: Mapped[Syllabus | None] = relationship(back_populates="exams")
    questions: Mapped[list[ExamQuestion]] = relationship(
        back_populates="exam",
        cascade="all, delete-orphan",
        order_by="ExamQuestion.position",
    )


class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    __table_args__ = (UniqueConstraint("exam_id", "question_id", name="uq_exam_question"),)

    exam_id: Mapped[int] = mapped_column(
        ForeignKey("exams.id", ondelete="CASCADE"),
        primary_key=True,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    is_reserve: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    exam: Mapped[Exam] = relationship(back_populates="questions")


class TestSession(Base):
    __tablename__ = "test_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    mode: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")
    scoring_rule_id: Mapped[int | None] = mapped_column(
        ForeignKey("scoring_rules.id"),
        nullable=True,
    )
    exam_id: Mapped[int | None] = mapped_column(ForeignKey("exams.id"), nullable=True)

    attempts: Mapped[list[TestAttempt]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class TestAttempt(Base):
    __tablename__ = "test_attempts"
    __table_args__ = (
        UniqueConstraint("test_session_id", "question_id", name="uq_attempt_session_question"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    test_session_id: Mapped[str] = mapped_column(
        ForeignKey("test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
        nullable=False,
    )
    selected_option_id: Mapped[int | None] = mapped_column(
        ForeignKey("question_options.id"),
        nullable=True,
    )
    is_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    answered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    session: Mapped[TestSession] = relationship(back_populates="attempts")
