#!/usr/bin/env python3
"""Script CLI para ejecutar la resolución automática de enlaces pregunta-apunte por coincidencia de tema.

Vía (a):
- Consume test-engine vía HTTP para obtener question_syllabus_tags.
- Consume apuntes-service vía HTTP para obtener el catálogo de notas.
- Resuelve temas con extract_block_and_topic.
- Persiste los enlaces en linking.sqlite.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Asegurar importación de linking-service
SERVICE_ROOT = Path(__file__).resolve().parent.parent
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from config import APUNTES_SERVICE_URL, SQLITE_PATH, SYLLABUS_TO_PROCESS_MAP, TEST_ENGINE_URL
from domain.service import LinkingService
from infrastructure.clients.apuntes_client import ApuntesClient
from infrastructure.clients.test_engine_client import TestEngineClient
from infrastructure.db.engine import get_connection, init_db
from infrastructure.db.repository import QuestionNoteLinkRepository


def run_resolution(
    syllabus_id: str,
    process_slug: str,
    db_path: Path,
    apuntes_url: str,
    test_engine_url: str,
) -> dict:
    init_db(db_path)
    conn = get_connection(db_path)
    repo = QuestionNoteLinkRepository(conn)
    apuntes_client = ApuntesClient(apuntes_url)
    test_engine_client = TestEngineClient(test_engine_url)

    service = LinkingService(
        repo=repo,
        apuntes_client=apuntes_client,
        test_engine_client=test_engine_client,
    )

    result = service.resolve_topic_matches(
        syllabus_id=syllabus_id,
        process_slug=process_slug,
    )
    conn.close()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolución automática de enlaces pregunta-apunte.")
    parser.add_argument("--syllabus-id", default="age-gsi-official", help="Identificador del temario")
    parser.add_argument("--process-slug", default="", help="Slug del proceso en apuntes-service")
    parser.add_argument("--db-path", default=str(SQLITE_PATH), help="Ruta a linking.sqlite")
    parser.add_argument("--apuntes-url", default=APUNTES_SERVICE_URL, help="URL de apuntes-service")
    parser.add_argument("--test-engine-url", default=TEST_ENGINE_URL, help="URL de test-engine")

    args = parser.parse_args()

    process_slug = args.process_slug
    if not process_slug:
        process_slug = SYLLABUS_TO_PROCESS_MAP.get(args.syllabus_id, "")
        if not process_slug:
            print(f"Error: No se encontró mapeo para syllabus_id='{args.syllabus_id}'. Especifica --process-slug.", file=sys.stderr)
            sys.exit(1)

    print(f"Iniciando resolución para '{args.syllabus_id}' contra '{process_slug}'...")
    print(f"  - Apuntes Service: {args.apuntes_url}")
    print(f"  - Test Engine:     {args.test_engine_url}")
    print(f"  - Base de datos:   {args.db_path}")

    res = run_resolution(
        syllabus_id=args.syllabus_id,
        process_slug=process_slug,
        db_path=Path(args.db_path),
        apuntes_url=args.apuntes_url,
        test_engine_url=args.test_engine_url,
    )

    print("\n" + "=" * 55)
    print("RESULTADO DE RESOLUCIÓN POR TEMA")
    print("=" * 55)
    print(f"Total preguntas evaluadas (tema no nulo): {res['total_evaluated']}")
    print(f"  - Resueltas a exactamente 1 nota:        {res['exact_matches']} (confianza: 1.0)")
    print(f"  - Resueltas a múltiples notas:           {res['multi_matches']} (confianza: 0.8)")
    print(f"  - Preguntas con 0 coincidencias:         {res['zero_matches']}")
    print(f"Total enlaces guardados en BD:            {res['links_created']}")
    print("=" * 55)

    if res["zero_matches"] > 0:
        print("\nPreguntas sin coincidencia (requieren sugerencia semántica):")
        for z in res["zero_questions"]:
            print(f"  - Pregunta ID {z['question_id']}: Bloque {z['block']}, Tema {z['topic']}")


if __name__ == "__main__":
    main()
