"""Iniciar sesión, registrar respuesta, cerrar y calcular resultado."""

from __future__ import annotations

from datetime import datetime, timezone

from domain.sessions.models import TestSession


class TestSessionService:
    def __init__(self, session_repository, scoring_service) -> None:
        self._sessions = session_repository
        self._scoring = scoring_service

    def remaining_seconds(self, session: TestSession, now: datetime | None = None) -> int | None:
        """Autoridad de tiempo en servidor (decisión c). None = sin cronómetro."""
        if session.duration_seconds is None:
            return None
        clock = now or datetime.now(timezone.utc)
        started = session.started_at
        if started.tzinfo is None:
            started = started.replace(tzinfo=timezone.utc)
        elapsed = (clock - started).total_seconds()
        remaining = int(session.duration_seconds - elapsed)
        return max(0, remaining)

    def is_expired(self, session: TestSession, now: datetime | None = None) -> bool:
        remaining = self.remaining_seconds(session, now)
        return remaining is not None and remaining <= 0
