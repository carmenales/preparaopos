#!/usr/bin/env python3
"""Copia de seguridad de la BD de test-engine con la API de backup de SQLite.

- Copia consistente aunque el servicio esté en marcha (no copia el fichero a pelo).
- Destino: backups/test-engine/ en la raíz del repo (fuera del bind mount de Docker
  y en .gitignore).
- Verifica la copia con PRAGMA integrity_check y conserva las N más recientes.

Uso:
    python scripts/backup_test_engine.py
    python scripts/backup_test_engine.py --keep 30 --label antes-de-purga
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "services" / "test-engine" / "data" / "test_engine.sqlite"
DEFAULT_DIR = REPO_ROOT / "backups" / "test-engine"
DEFAULT_KEEP = 14


def backup_database(db_path: Path, backup_dir: Path, label: str | None = None) -> Path:
    if not db_path.exists():
        raise FileNotFoundError(f"No existe la BD: {db_path}")

    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = f"_{label}" if label else ""
    target = backup_dir / f"test_engine_{stamp}{suffix}.sqlite"

    src = sqlite3.connect(db_path, timeout=30)
    dst = sqlite3.connect(target)
    try:
        src.backup(dst)
    except Exception:
        dst.close()
        src.close()
        for leftover in (target, target.with_name(target.name + "-journal")):
            leftover.unlink(missing_ok=True)
        raise
    dst.close()
    src.close()

    check = sqlite3.connect(target)
    try:
        result = check.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        check.close()
    if result != "ok":
        target.unlink(missing_ok=True)
        raise RuntimeError(f"La copia no pasa integrity_check: {result}")

    return target


def prune_backups(backup_dir: Path, keep: int) -> list[Path]:
    backups = sorted(backup_dir.glob("test_engine_*.sqlite"), key=lambda p: p.stat().st_mtime, reverse=True)
    removed = backups[keep:]
    for old in removed:
        old.unlink()
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Copia de seguridad de la BD de test-engine.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--keep", type=int, default=DEFAULT_KEEP, help="Copias a conservar (por defecto 14)")
    parser.add_argument("--label", help="Sufijo descriptivo para el nombre del fichero")
    args = parser.parse_args()

    try:
        target = backup_database(args.db, args.dir, args.label)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    size_mb = target.stat().st_size / 1_048_576
    print(f"[ok] Copia verificada: {target} ({size_mb:.1f} MB)")
    for old in prune_backups(args.dir, args.keep):
        print(f"[borrada] {old.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
