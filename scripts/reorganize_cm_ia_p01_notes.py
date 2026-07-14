#!/usr/bin/env python3
"""
Reorganiza apuntes Markdown existentes del perfil P01 de IA.

Uso desde la raíz del repositorio:

    python scripts/reorganize_cm_ia_p01_notes.py

Primero hace dry-run. Para aplicar cambios reales:

    python scripts/reorganize_cm_ia_p01_notes.py --apply

No requiere dependencias externas.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_SOURCE_DIR = Path("knowledge/processes/comunidad-madrid/administracion-digital")
DEFAULT_TARGET_DIR = Path(
    "knowledge/processes/comunidad-madrid/administracion-digital"
    "/ia/profiles/p01-consultor-sistemas-informacion-ia/apuntes"
)
DEFAULT_P02_DIR = Path(
    "knowledge/processes/comunidad-madrid/administracion-digital"
    "/ia/profiles/p02-consultor-sistemas-informacion-gobierno-ia/apuntes"
)

PROCESS_SLUG = "comunidad-madrid/administracion-digital/ia"
PROFILE_SLUG = "p01-consultor-sistemas-informacion-ia"
OFFICIAL_PROFILE = (
    "P01 - Consultor de Sistemas de Información - "
    "IA Aplicada al Ciclo de Vida del Software"
)
ID_PREFIX = "cm-ad-ia-p01"


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    text = normalize_newlines(text)

    if not text.startswith("---\n"):
        return None, text

    end = text.find("\n---", 4)

    if end == -1:
        return None, text

    frontmatter = text[4:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")

    return frontmatter, body


def strip_yaml_quotes(value: str) -> object:
    value = value.strip()

    if value in {"null", "Null", "NULL", "~"}:
        return None

    if value in {"true", "True", "TRUE"}:
        return True

    if value in {"false", "False", "FALSE"}:
        return False

    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    return value


def parse_simple_frontmatter(frontmatter: str | None) -> dict[str, object]:
    if not frontmatter:
        return {}

    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()

        if not line.strip() or line.lstrip().startswith("#"):
            continue

        stripped = line.strip()

        if stripped.startswith("- ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(strip_yaml_quotes(stripped[2:].strip()))
            continue

        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key

            if value == "":
                data[key] = []
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                data[key] = [] if not inner else [
                    strip_yaml_quotes(part.strip()) for part in inner.split(",")
                ]
            else:
                data[key] = strip_yaml_quotes(value)

    return data


def quote_yaml(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def format_yaml_value(value: object) -> str:
    if value is None:
        return "null"

    if isinstance(value, bool):
        return "true" if value else "false"

    return quote_yaml(str(value))


def dump_frontmatter(data: dict[str, object]) -> str:
    preferred_order = [
        "id",
        "title",
        "type",
        "status",
        "processes",
        "profiles",
        "official_profile",
        "official_topic",
        "source_ids",
        "tags",
        "created_at",
        "last_reviewed",
        "ai_generated",
        "ai_sources",
        "needs_human_review",
    ]

    ordered_keys = [key for key in preferred_order if key in data]
    ordered_keys.extend(key for key in data.keys() if key not in ordered_keys)

    lines = ["---"]

    for key in ordered_keys:
        value = data[key]

        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {format_yaml_value(item)}")
        else:
            lines.append(f"{key}: {format_yaml_value(value)}")

    lines.append("---")

    return "\n".join(lines)


def note_topic_slug(path: Path) -> str:
    stem = path.stem

    if stem.startswith("p01-"):
        stem = stem[4:]

    return stem


def new_file_name(path: Path) -> str:
    if path.name.startswith("p01-"):
        return path.name

    return f"p01-{path.name}"


def new_note_id(path: Path) -> str:
    return f"{ID_PREFIX}-{note_topic_slug(path)}"


def should_migrate(path: Path, source_dir: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False

    if path.name.lower() == "readme.md":
        return False

    if "ia" in path.relative_to(source_dir).parts:
        return False

    return bool(re.match(r"^(p01-)?tema-[0-9]{3}-.+\.md$", path.name))


def update_note_content(content: str, source_path: Path) -> str:
    frontmatter, body = split_frontmatter(content)
    data = parse_simple_frontmatter(frontmatter)

    data["id"] = new_note_id(source_path)
    data.setdefault("title", source_path.stem.replace("-", " ").title())
    data.setdefault("type", "apunte")
    data.setdefault("status", "borrador")
    data["processes"] = [PROCESS_SLUG]
    data["profiles"] = [PROFILE_SLUG]
    data["official_profile"] = OFFICIAL_PROFILE

    data.setdefault("source_ids", [])
    data.setdefault("tags", [])
    data.setdefault("last_reviewed", None)
    data.setdefault("ai_generated", True)
    data.setdefault("ai_sources", [])
    data.setdefault("needs_human_review", True)

    return dump_frontmatter(data) + "\n\n" + body.rstrip() + "\n"


def ensure_directories(apply: bool, directories: list[Path]) -> None:
    for directory in directories:
        if apply:
            directory.mkdir(parents=True, exist_ok=True)
        print(f"{'CREATE' if apply else 'WOULD CREATE'} {directory}")


def migrate_notes(source_dir: Path, target_dir: Path, p02_dir: Path, apply: bool) -> int:
    ensure_directories(apply, [target_dir, p02_dir])

    candidates = sorted(
        path for path in source_dir.rglob("*.md") if should_migrate(path, source_dir)
    )

    if not candidates:
        print("No se han encontrado apuntes candidatos.")
        return 0

    migrated = 0

    for source_path in candidates:
        target_path = target_dir / new_file_name(source_path)
        content = source_path.read_text(encoding="utf-8")
        updated = update_note_content(content, source_path)

        print(f"{'MOVE' if apply else 'WOULD MOVE'} {source_path} -> {target_path}")
        print(f"  new id: {new_note_id(source_path)}")
        print(f"  profile: {PROFILE_SLUG}")

        if apply:
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if target_path.exists():
                raise FileExistsError(f"Ya existe el destino: {target_path}")

            target_path.write_text(updated, encoding="utf-8")
            source_path.unlink()

        migrated += 1

    return migrated


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reorganiza apuntes P01 IA y actualiza frontmatter."
    )
    parser.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    parser.add_argument("--target-dir", default=str(DEFAULT_TARGET_DIR))
    parser.add_argument("--p02-dir", default=str(DEFAULT_P02_DIR))
    parser.add_argument("--apply", action="store_true")

    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    target_dir = Path(args.target_dir)
    p02_dir = Path(args.p02_dir)

    if not source_dir.exists():
        raise FileNotFoundError(f"No existe source-dir: {source_dir}")

    print(f"Modo: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Origen: {source_dir}")
    print(f"Destino P01: {target_dir}")
    print(f"Scaffold P02: {p02_dir}")
    print()

    migrated = migrate_notes(source_dir, target_dir, p02_dir, args.apply)

    print()
    print(f"Apuntes procesados: {migrated}")

    if not args.apply:
        print()
        print("No se ha modificado nada. Para aplicar:")
        print("python scripts/reorganize_cm_ia_p01_notes.py --apply")
    else:
        print()
        print("Cambios aplicados. Recomendado ahora:")
        print("python scripts/build_knowledge_index.py")
        print("git status --short")


if __name__ == "__main__":
    main()
