"""Datos y validación de los formularios de gestión de preguntas y cuestionarios."""

from __future__ import annotations

from dataclasses import dataclass

MIN_OPTIONS = 2
MAX_OPTIONS = 6


class ValidationError(ValueError):
    """Errores de formulario, en español, para mostrarlos tal cual."""

    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


@dataclass
class OptionInput:
    text: str
    justification: str | None = None
    option_id: int | None = None  # None = opción nueva


@dataclass
class QuestionInput:
    statement: str
    options: list[OptionInput]
    correct_index: int | None
    justification: str | None = None
    syllabus_id: str | None = None
    block: str | None = None
    topic: str | None = None
    year: int | None = None
    is_official_exam: bool = False
    is_annulled: bool = False
    annulment_reason: str | None = None
    add_to_exam_id: int | None = None

    def validate(self) -> None:
        errors: list[str] = []
        if not self.statement.strip():
            errors.append("El enunciado es obligatorio.")
        if len(self.options) < MIN_OPTIONS:
            errors.append(f"Hacen falta al menos {MIN_OPTIONS} opciones con texto.")
        if len(self.options) > MAX_OPTIONS:
            errors.append(f"Como máximo {MAX_OPTIONS} opciones.")
        if self.correct_index is None or not 0 <= self.correct_index < len(self.options):
            errors.append("Marca cuál es la opción correcta (y que tenga texto).")
        texts = [o.text.strip().lower() for o in self.options]
        if len(set(texts)) != len(texts):
            errors.append("Hay opciones repetidas.")
        if not self.syllabus_id:
            errors.append("Elige el temario.")
        if self.topic and not self.block:
            errors.append("Para indicar el tema hay que indicar también el bloque.")
        if self.year is not None and not 1990 <= self.year <= 2100:
            errors.append("El año no es válido.")
        if self.is_annulled and not (self.annulment_reason or "").strip():
            errors.append("Indica el motivo de la anulación.")
        if errors:
            raise ValidationError(errors)


@dataclass
class ExamInput:
    name: str
    syllabus_id: str | None
    year: int | None = None
    convocatoria: str | None = None
    scoring_rule_id: int | None = None
    duration_minutes: int | None = None

    def validate(self) -> None:
        errors: list[str] = []
        if not self.name.strip():
            errors.append("El nombre es obligatorio.")
        if len(self.name) > 255:
            errors.append("El nombre no puede pasar de 255 caracteres.")
        if not self.syllabus_id:
            errors.append("Elige el temario.")
        if self.year is not None and not 1990 <= self.year <= 2100:
            errors.append("El año no es válido.")
        if self.duration_minutes is not None and not 1 <= self.duration_minutes <= 600:
            errors.append("La duración debe estar entre 1 y 600 minutos.")
        if errors:
            raise ValidationError(errors)
