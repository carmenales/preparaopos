"""Base de conocimiento de prueba para los tests de study-assistant.

Los apuntes reales y su índice (apps/studyassistant/data/knowledge_index.json) no están en git,
así que los tests no pueden depender de ellos: en CI o en un clon limpio no existen. Aquí se crea,
antes de que se importe ``config``, un índice y unos ficheros Markdown mínimos en un directorio
temporal, y se apunta el servicio a ellos.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

if "config" in sys.modules:
    raise RuntimeError("config se importó antes de tests/conftest.py: los tests usarían los apuntes reales.")

_TMP_DIR = Path(tempfile.mkdtemp(prefix="study_assistant_"))
KNOWLEDGE_DIR = _TMP_DIR / "knowledge"
INDEX_PATH = _TMP_DIR / "knowledge_index.json"

NOTES = [
    {
        "id": "tema-i-01-derecho-constitucional",
        "title": "Tema I.01 Derecho Constitucional",
        "official_topic": "I.01 Derecho Constitucional",
        "path": "knowledge/processes/age/a2-gsi/apuntes/Tema I.01 Derecho Constitucional.md",
        "processes": ["age/a2-gsi"],
        "status": "revisado",
        "tags": ["constitucion"],
        "body": "## 1. Introducción\n\nLa Constitución Española de 1978.\n\n## 2. Derechos\n\nTexto.\n",
    },
    {
        "id": "tema-i-02-derechoconstitucional",
        "title": "Tema I.02 Derecho Constitucional",
        "official_topic": "Tema I.02 Derecho Constitucional",
        "path": "knowledge/processes/age/a2-gsi/apuntes/Tema I.02 Derecho Constitucional.md",
        "processes": ["age/a2-gsi"],
        "status": "borrador",
        "tags": ["constitucion"],
        "body": "## 1. El Gobierno\n\nTexto.\n",
    },
    {
        "id": "majadahonda-operador-tema-05-ens",
        "title": "Tema 5. Esquema Nacional de Seguridad",
        "official_topic": "Tema 5. Esquema Nacional de Seguridad",
        "path": "knowledge/processes/ayuntamiento-majadahonda/apuntes/tema-05-ens.md",
        "processes": ["ayuntamiento-majadahonda"],
        "status": "borrador",
        "tags": ["ens"],
        "body": "## 1. Ámbito\n\nTexto.\n",
    },
]


def _build_fixture() -> None:
    index_notes = []
    for n in NOTES:
        target = KNOWLEDGE_DIR / Path(*Path(n["path"]).parts[1:])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"---\nid: \"{n['id']}\"\ntitle: \"{n['title']}\"\n---\n\n{n['body']}", encoding="utf-8")
        headings = [{"level": 2, "text": line[3:], "anchor": line[3:].lower().replace(" ", "-").replace(".", "")}
                    for line in n["body"].splitlines() if line.startswith("## ")]
        index_notes.append({k: v for k, v in n.items() if k != "body"} | {
            "slug": n["id"], "headings": headings, "excerpt": n["body"][:80], "content_text": n["body"],
            "practice": {}, "block": None,
        })
    processes = {p: {"id": p, "title": p, "organism": ""} for n in NOTES for p in n["processes"]}
    INDEX_PATH.write_text(json.dumps({"generated_at": "2026-01-01T00:00:00Z", "processes": processes,
                                      "notes": index_notes}, ensure_ascii=False), encoding="utf-8")


_build_fixture()
os.environ["KNOWLEDGE_BASE_PATH"] = str(KNOWLEDGE_DIR)
os.environ["KNOWLEDGE_INDEX_PATH"] = str(INDEX_PATH)


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(_TMP_DIR, ignore_errors=True)
