"""
Genera apuntes Markdown consumibles a partir de ficheros fuente o Markdown previo.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

TEMPLATE_DEFAULT = Path("knowledge/_template/apunte-fuente-privada.md")
CONFIG_DEFAULT = Path("knowledge-note-generator.yml")
SUPPORTED_EXTENSIONS = {".md", ".txt"}


@dataclass(frozen=True)
class NoteMetadata:
    id: str
    title: str
    type: str
    status: str
    processes: list[str]
    profile: str
    source: str
    shared_with: list[str]
    official_topic: str
    source_ids: list[str]
    tags: list[str]
    created_at: str
    last_reviewed: str | None
    ai_generated: bool
    ai_cleaned: bool
    ai_sources: list[str]
    needs_human_review: bool


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("/", "-")
    value = re.sub(r"[^a-z0-9áéíóúüñ\-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def split_frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        return [], text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return [], text
    return parts[1].splitlines(), parts[2].lstrip("\n")


def load_yaml_config(path: Path) -> dict:
    if not path.exists():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML no está instalado. Instálalo o elimina el uso de config YAML.")
    data = yaml.safe_load(read_text(path))
    return data or {}


def load_template_keys(path: Path) -> list[str]:
    frontmatter_lines, _ = split_frontmatter(read_text(path))
    if not frontmatter_lines:
        raise ValueError(f"La plantilla {path} no contiene frontmatter YAML válido.")
    if yaml is None:
        raise RuntimeError("PyYAML no está instalado. Instálalo para poder leer plantillas.")

    frontmatter_text = "\n".join(frontmatter_lines)
    parsed = yaml.safe_load(frontmatter_text) or {}
    return list(parsed.keys())


def build_process_path(process_value: str, profile_value: str) -> str:
    parts = [part for part in [process_value, profile_value] if part and part != "shared"]
    return "/".join(parts)


def default_title_from_path(source_path: Path) -> str:
    title = source_path.stem.replace("_", " ").replace("-", " ").strip()
    title = re.sub(r"\s+", " ", title)
    return title or source_path.stem


def infer_process_profile(relative_parts: tuple[str, ...], fallback_process: str, fallback_profile: str) -> tuple[str, str]:
    if len(relative_parts) >= 2:
        return relative_parts[0], relative_parts[1]
    if len(relative_parts) == 1:
        return relative_parts[0], fallback_profile
    return fallback_process, fallback_profile

def infer_official_topic(source_path: Path, explicit_topic: str | None) -> str:
    if explicit_topic is not None:
        return explicit_topic
    match = re.search(r"(?:tema|topic)\s*([\w.-]+)", source_path.stem, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def parse_list_arg(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def bool_from_value(value, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y", "si", "sí"}:
            return True
        if lowered in {"false", "0", "no", "n"}:
            return False
    return default


def merge_config(config: dict, profile_key: str | None, shared_key: str | None, cli: dict) -> dict:
    defaults = (config.get("defaults") or {}).copy()
    if profile_key:
        profiles = config.get("profiles") or {}
        if profile_key not in profiles:
            raise KeyError(f"No existe el profile_key en el YAML: {profile_key}")
        defaults.update(profiles[profile_key])
    if shared_key:
        shared = config.get("shared") or {}
        if shared_key not in shared:
            raise KeyError(f"No existe el shared_key en el YAML: {shared_key}")
        defaults.update(shared[shared_key])

    merged = defaults
    for key, value in cli.items():
        if value is not None:
            merged[key] = value
    return merged


def build_metadata(
    source_path: Path,
    input_root: Path,
    settings: dict,
) -> NoteMetadata:
    relative = source_path.relative_to(input_root)
    parts = relative.parts[:-1] if source_path.is_file() and source_path.suffix.lower() in SUPPORTED_EXTENSIONS else relative.parts
    title = settings.get("title") or default_title_from_path(source_path)
    fallback_process = settings.get("process") or "age"
    fallback_profile = settings.get("profile") or ""
    inferred_process, inferred_profile = infer_process_profile(parts, fallback_process, fallback_profile)
    process_value = settings.get("process") or inferred_process
    profile_value = settings.get("profile") or inferred_profile
    processes_path = build_process_path(process_value, profile_value)
    source_value = settings.get("source") or ""
    official_topic_value = infer_official_topic(source_path, settings.get("official_topic"))
    tags = settings.get("tags") or []
    shared_with = settings.get("shared_with") or []
    return NoteMetadata(
        id=slugify(source_path.stem),
        title=title,
        type="apunte",
        status=settings.get("status") or "borrador",
        processes=[processes_path] if processes_path else [],
        profile=profile_value,
        source=source_value,
        shared_with=shared_with,
        official_topic=official_topic_value,
        source_ids=settings.get("source_ids") or [],
        tags=tags,
        created_at=date.today().isoformat(),
        last_reviewed=None,
        ai_generated=bool_from_value(settings.get("ai_generated"), False),
        ai_cleaned=bool_from_value(settings.get("ai_cleaned"), True),
        ai_sources=settings.get("ai_sources") or [],
        needs_human_review=bool_from_value(settings.get("needs_human_review"), True),
    )


def render_scalar(value: str | None) -> str:
    if value is None:
        return "null"
    return f'"{value}"'


def render_list(values: Iterable[str]) -> list[str]:
    values = list(values)
    if not values:
        return ["[]"]
    return ["", *[f'  - "{item}"' for item in values]]


def render_frontmatter(template_keys: list[str], metadata: NoteMetadata) -> list[str]:
    output: list[str] = []
    for key in template_keys:
        if key == "id":
            output.append(f'id: "{metadata.id}"')
        elif key == "title":
            output.append(f'title: "{metadata.title}"')
        elif key == "type":
            output.append(f'type: "{metadata.type}"')
        elif key == "status":
            output.append(f'status: "{metadata.status}"')
        elif key == "processes":
            output.append("processes: []" if not metadata.processes else "processes:")
            output.extend([f'  - "{item}"' for item in metadata.processes])
        elif key == "profile":
            output.append(f'profile: {render_scalar(metadata.profile)}')
        elif key == "source":
            output.append(f'source: {render_scalar(metadata.source)}')
        elif key == "shared_with":
            output.append("shared_with: []" if not metadata.shared_with else "shared_with:")
            if metadata.shared_with:
                output.extend([f'  - "{item}"' for item in metadata.shared_with])
        elif key == "official_topic":
            output.append(f'official_topic: {render_scalar(metadata.official_topic)}')
        elif key == "source_ids":
            output.append("source_ids: []" if not metadata.source_ids else "source_ids:")
            if metadata.source_ids:
                output.extend([f'  - "{src}"' for src in metadata.source_ids])
        elif key == "tags":
            output.append("tags: []" if not metadata.tags else "tags:")
            if metadata.tags:
                output.extend([f'  - "{tag}"' for tag in metadata.tags])
        elif key == "created_at":
            output.append(f'created_at: "{metadata.created_at}"')
        elif key == "last_reviewed":
            output.append("last_reviewed: null")
        elif key == "ai_generated":
            output.append(f'ai_generated: {str(metadata.ai_generated).lower()}')
        elif key == "ai_cleaned":
            output.append(f'ai_cleaned: {str(metadata.ai_cleaned).lower()}')
        elif key == "ai_sources":
            output.append("ai_sources: []" if not metadata.ai_sources else "ai_sources:")
            if metadata.ai_sources:
                output.extend([f'  - "{src}"' for src in metadata.ai_sources])
        elif key == "needs_human_review":
            output.append(f'needs_human_review: {str(metadata.needs_human_review).lower()}')
        else:
            print(f"[aviso] La plantilla tiene la clave '{key}', que este script no sabe rellenar. Se deja a null.")
            output.append(f"{key}: null")
    return output


def build_note(template_path: Path, metadata: NoteMetadata, body: str) -> str:
    template_keys = load_template_keys(template_path)
    rendered_frontmatter = render_frontmatter(template_keys, metadata)
    body = body.lstrip("\n")
    return "---\n" + "\n".join(rendered_frontmatter) + "\n---\n\n" + f"# {metadata.title}\n\n" + body.rstrip() + "\n"


def collect_inputs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    return sorted(p for p in input_path.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)


def process_file(
    source_path: Path,
    input_root: Path,
    output_root: Path,
    template_path: Path,
    settings: dict,
    overwrite: bool,
) -> Path:
    metadata = build_metadata(source_path=source_path, input_root=input_root, settings=settings)
    relative = source_path.relative_to(input_root).with_suffix(".md")
    output_path = output_root / relative
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Ya existe: {output_path}. Usa --overwrite para reemplazarlo.")
    body = read_text(source_path)
    write_text(output_path, build_note(template_path, metadata, body))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera apuntes Markdown consumibles con frontmatter.")
    parser.add_argument("input_path", help="Archivo o carpeta de entrada")
    parser.add_argument("output_root", help="Carpeta raíz de salida")
    parser.add_argument("--config", default=str(CONFIG_DEFAULT), help="Ruta del fichero YAML de configuración.")
    parser.add_argument("--template", default=None, help="Ruta de la plantilla de apunte.")
    parser.add_argument("--profile-key", default=None, help="Clave de perfil del YAML, por ejemplo age/a2-gsi-cetic.")
    parser.add_argument("--shared-key", default=None, help="Clave compartida del YAML, por ejemplo legal/normativa-general.")
    parser.add_argument("--process", default=None, help="Proceso destino, por ejemplo age.")
    parser.add_argument("--profile", default=None, help="Perfil de oposición, por ejemplo a2-gsi.")
    parser.add_argument("--source", default=None, help="Fuente concreta, por ejemplo cetic o preparatic.")
    parser.add_argument("--shared-with", default=None, help="Lista de perfiles con los que se comparte, separada por comas.")
    parser.add_argument("--official-topic", default=None, help="Tema oficial o identificador equivalente.")
    parser.add_argument("--status", default=None, help="Estado del apunte.")
    parser.add_argument("--title", default=None, help="Título explícito del apunte.")
    parser.add_argument("--tags", default=None, help="Lista de tags separada por comas.")
    parser.add_argument("--source-ids", default=None, help="IDs de fuentes separadas por comas.")
    parser.add_argument("--ai-sources", default=None, help="Fuentes IA separadas por comas.")
    parser.add_argument("--ai-generated", default=None, help="Marca el apunte como generado por IA.")
    parser.add_argument("--ai-cleaned", default=None, help="Marca el apunte como limpiado con IA.")
    parser.add_argument("--needs-human-review", default=None, help="Marca el apunte como pendiente de revisión humana.")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribe si el destino ya existe.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path)
    output_root = Path(args.output_root)
    config_path = Path(args.config)

    if not input_path.exists():
        raise FileNotFoundError(f"No existe la ruta de entrada: {input_path}")
    if not config_path.exists():
        raise FileNotFoundError(f"No existe el fichero de configuración: {config_path}")

    config = load_yaml_config(config_path)
    template_path = Path(args.template or ((config.get("defaults") or {}).get("template") or TEMPLATE_DEFAULT))
    if not template_path.exists():
        raise FileNotFoundError(f"No existe la plantilla: {template_path}")

    inputs = collect_inputs(input_path)
    if not inputs:
        print("No se han encontrado ficheros compatibles.")
        return

    cli_settings = {
        "source": args.source,
        "process": args.process,
        "profile": args.profile,
        "shared_with": parse_list_arg(args.shared_with),
        "official_topic": args.official_topic,
        "status": args.status,
        "title": args.title,
        "tags": parse_list_arg(args.tags),
        "source_ids": parse_list_arg(args.source_ids),
        "ai_sources": parse_list_arg(args.ai_sources),
        "ai_generated": args.ai_generated,
        "ai_cleaned": args.ai_cleaned,
        "needs_human_review": args.needs_human_review,
    }

    merged_settings = merge_config(config, args.profile_key, args.shared_key, cli_settings)

    input_root = input_path if input_path.is_dir() else input_path.parent
    for source in inputs:
        out = process_file(
            source_path=source,
            input_root=input_root,
            output_root=output_root,
            template_path=template_path,
            settings=merged_settings,
            overwrite=args.overwrite,
        )
        print(f"[ok] {source} -> {out}")


if __name__ == "__main__":
    main()
