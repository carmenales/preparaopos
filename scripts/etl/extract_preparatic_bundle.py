"""
Script ETL para extraer y deduplicar las preguntas y el catálogo temático
embebidos en el bundle Vite de PreparaTIC (apps/tests_preparatic/v3/index.html).

Salidas:
  - scripts/etl/preparatic_bundle_extracted.json (array de preguntas deduplicadas)
  - scripts/etl/preparatic_catalog.json (catálogo de 8 bloques y 133 temas)

Ejecución:
  python scripts/etl/extract_preparatic_bundle.py
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
from collections import OrderedDict
from pathlib import Path

try:
    import json5
except ImportError:
    print("ERROR: json5 no está instalado. Ejecuta: pip install json5")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("extract_preparatic")


def extract_bracket_range(data: bytes, start: int) -> tuple[bytes, int]:
    """Extrae el rango completo del array delimitado por '[' y ']' respetando comillas y escapes.

    Args:
        data: Buffer binario completo del archivo.
        start: Posición del '[' de apertura.

    Returns:
        Tupla con (bytes del array extraído, índice inmediatamente posterior al ']' de cierre).
    """
    depth = 0
    in_str = False
    quote: int | None = None
    i = start
    n = len(data)

    while i < n:
        c = data[i]
        if in_str:
            if c == 92:  # Carácter de escape '\'
                i += 2
                continue
            if c == quote:
                in_str = False
        else:
            if c in (34, 39, 96):  # Comillas dobles (34), simples (39) o backticks (96)
                in_str = True
                quote = c
            elif c == 91:  # '['
                depth += 1
            elif c == 93:  # ']'
                depth -= 1
                if depth == 0:
                    i += 1
                    break
        i += 1

    return data[start:i], i


def extract_catalog(data: bytes) -> tuple[list[dict], list[dict]]:
    """Extrae el catálogo oficial de bloques y temas embebido en el bundle.

    Returns:
        Tupla con (lista de bloques, lista de temas).
    """
    logger.info("Localizando catálogo de bloques y temas en el bundle...")

    # 1. Bloques
    m_block = re.search(rb'\[\{name:\"A1\",title:\"[^\"]+\"', data)
    blocks: list[dict] = []
    if m_block:
        start = m_block.start()
        arr_bytes, _ = extract_bracket_range(data, start)
        raw_text = arr_bytes.decode("utf-8", errors="ignore")
        blocks = json5.loads(raw_text)
        logger.info("Catálogo: extraídos %d bloques.", len(blocks))
    else:
        logger.warning("No se encontró el ancla de inicio del catálogo de bloques.")

    # 2. Temas
    m_topic = re.search(rb'\[\{id:\"1\",name:\"[^\"]+\",block:\"A1\"\}', data)
    topics: list[dict] = []
    if m_topic:
        start = m_topic.start()
        arr_bytes, _ = extract_bracket_range(data, start)
        raw_text = arr_bytes.decode("utf-8", errors="ignore")
        topics = json5.loads(raw_text)
        logger.info("Catálogo: extraídos %d temas.", len(topics))
    else:
        logger.warning("No se encontró el ancla de inicio del catálogo de temas.")

    return blocks, topics


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    bundle_path = repo_root / "apps" / "tests_preparatic" / "v3" / "index.html"
    output_questions_path = repo_root / "scripts" / "etl" / "preparatic_bundle_extracted.json"
    output_catalog_path = repo_root / "scripts" / "etl" / "preparatic_catalog.json"

    if not bundle_path.is_file():
        logger.error("No se encontró el bundle en: %s", bundle_path)
        sys.exit(1)

    t0 = time.time()
    logger.info("Leyendo bundle Vite: %s (%s MB)...", bundle_path.name, f"{bundle_path.stat().st_size / (1024*1024):.1f}")
    data = bundle_path.read_bytes()

    # 1. Extraer catálogo de bloques y temas
    blocks, topics = extract_catalog(data)

    # 2. Localizar todas las ocurrencias de arrays de preguntas
    logger.info("Buscando todos los fragmentos de preguntas en el bundle...")
    start_arr_pattern = re.compile(rb'\[\s*\{\s*id:\"(\d+)\",\s*text:\"')
    matches = list(start_arr_pattern.finditer(data))
    total_fragments = len(matches)
    logger.info("Localizados %d fragmentos de arrays de preguntas.", total_fragments)

    if total_fragments == 0:
        logger.error("No se localizó ningún fragmento de preguntas con el patrón esperado.")
        sys.exit(1)

    # 3. Extraer, desminificar Terser (!0/!1), parsear y deduplicar
    all_questions: dict[str, dict] = OrderedDict()
    seen_chunk_hashes: set[int] = set()
    total_objects_before_dedup = 0
    parse_errors = 0
    skipped_duplicate_chunks = 0

    logger.info("Extrayendo y parseando fragmentos con json5...")
    for idx, match in enumerate(matches, 1):
        start = match.start()
        arr_bytes, _ = extract_bracket_range(data, start)

        # Optimización: si el chunk de bytes es idéntico a uno ya procesado, saltar el parseo costoso de json5
        chunk_hash = hash(arr_bytes)
        if chunk_hash in seen_chunk_hashes:
            skipped_duplicate_chunks += 1
            if idx % 100 == 0 or idx == total_fragments:
                logger.info(
                    "Progreso: %d/%d fragmentos (saltados %d chunks duplicados por build, preguntas únicas: %d)...",
                    idx,
                    total_fragments,
                    skipped_duplicate_chunks,
                    len(all_questions),
                )
            continue
        seen_chunk_hashes.add(chunk_hash)

        raw_text = arr_bytes.decode("utf-8", errors="ignore")

        # Conversión segura de booleanos Terser (!0 / !1) acotada por lookarounds
        safe = re.sub(r"(?<=:)!0(?=[,}])", "true", raw_text)
        safe = re.sub(r"(?<=:)!1(?=[,}])", "false", safe)

        # Conversión de literales template en JS (backticks en respuestas como `awk ...`) a comillas simples
        safe = re.sub(r"answer:`([^`]*)`", r"answer:'\1'", safe)

        try:
            fragment_questions = json5.loads(safe)
            total_objects_before_dedup += len(fragment_questions)
            for q in fragment_questions:
                q_id = str(q.get("id", "")).strip()
                if q_id:
                    all_questions[q_id] = q
        except Exception as exc:
            parse_errors += 1
            logger.warning("Error parseando fragmento #%d (offset %d): %s", idx, start, exc)

        if idx % 100 == 0 or idx == total_fragments:
            logger.info(
                "Progreso: %d/%d fragmentos (saltados %d chunks duplicados por build, preguntas únicas: %d)...",
                idx,
                total_fragments,
                skipped_duplicate_chunks,
                len(all_questions),
            )

    unique_questions = list(all_questions.values())
    total_unique = len(unique_questions)

    # 4. Verificación y estadísticas del conjunto extraído
    distinct_blocks = sorted(list({q.get("block") for q in unique_questions if q.get("block")}))
    distinct_topics = sorted(list({str(q.get("topic")) for q in unique_questions if q.get("topic")}), key=lambda x: int(x) if x.isdigit() else 999)

    elapsed = time.time() - t0
    logger.info("=" * 65)
    logger.info("RESUMEN DE EXTRACCIÓN Y VERIFICACIÓN")
    logger.info("=" * 65)
    logger.info("Fragmentos localizados en el fichero : %d", total_fragments)
    logger.info("Chunks idénticos saltados por hash   : %d", skipped_duplicate_chunks)
    logger.info("Fragmentos parseados con json5       : %d", len(seen_chunk_hashes))
    logger.info("Fragmentos con error de parseo       : %d", parse_errors)
    logger.info("Total objetos-pregunta pre-dedup     : %d", total_objects_before_dedup)
    logger.info("Preguntas ÚNICAS tras deduplicar por id: %d", total_unique)
    logger.info("Bloques encontrados en las preguntas : %d (%s)", len(distinct_blocks), ", ".join(distinct_blocks))
    logger.info("Temas distintos en las preguntas     : %d (rango min=%s, max=%s)", len(distinct_topics), distinct_topics[0] if distinct_topics else "-", distinct_topics[-1] if distinct_topics else "-")
    logger.info("Catálogo oficial embebido            : %d bloques, %d temas", len(blocks), len(topics))
    logger.info("Tiempo total transcurrido            : %.2f segundos", elapsed)
    logger.info("=" * 65)

    # Verificación de umbral de seguridad
    if total_unique < 15000:
        logger.error(
            "ALERTA: Se esperaban ~16.673 preguntas únicas pero solo se obtuvieron %d. "
            "Revisa si algún fragmento quedó fuera del escaneo.",
            total_unique,
        )
        sys.exit(1)

    # 5. Volcar salida
    logger.info("Escribiendo preguntas extraídas en: %s...", output_questions_path)
    output_questions_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_questions_path, "w", encoding="utf-8") as f:
        json.dump(unique_questions, f, ensure_ascii=False, indent=2)

    logger.info("Escribiendo catálogo en: %s...", output_catalog_path)
    catalog_data = {
        "blocks": blocks,
        "topics": topics,
    }
    with open(output_catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, ensure_ascii=False, indent=2)

    logger.info(
        "¡Extracción completada con éxito! Generado %s (%.2f MB).",
        output_questions_path.name,
        output_questions_path.stat().st_size / (1024 * 1024),
    )


if __name__ == "__main__":
    main()
