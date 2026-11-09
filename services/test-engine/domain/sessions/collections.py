"""Colecciones de tests fijos: el menú «Tests» de PreparaTIC V3 (Aleatorios, Relevancia, Bloques, Temas, Años).

PreparaTIC no genera un test al azar cada vez: reparte el banco en tests numerados («Test Bloque A1 #3»)
que siempre tienen las mismas preguntas, para que se vea cuáles has hecho y con qué nota, e ir
avanzando hasta haberlas visto todas. Aquí cada test fijo es un filtro del generador con ``part``:
su ``source_ref`` lo identifica y las sesiones que lo han hecho se buscan por él.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from domain.sessions.generator import GeneratorFilters

# Preguntas por test (como el simulacro AGE A2 GSI) y tests de la colección «Relevancia».
COLLECTION_SIZE = 100
RELEVANCE_TESTS = 50


@dataclass(frozen=True)
class CollectionKind:
    slug: str
    menu: str      # texto del menú lateral
    title: str     # título de la página
    intro: str


KINDS: dict[str, CollectionKind] = {k.slug: k for k in (
    CollectionKind("random", "Aleatorios", "Tests aleatorios",
                   "Todo el temario repartido en tests de 100 preguntas al azar. Cada pregunta está en un solo "
                   "test: si los haces todos, habrás visto el banco entero."),
    CollectionKind("relevance", "Relevancia", "Tests por relevancia",
                   "Preguntas elegidas según lo que más ha caído en los exámenes oficiales: los temas que más "
                   "salen tienen más preguntas. Cada test es una muestra distinta y siempre la misma."),
    CollectionKind("blocks", "Bloques", "Tests por bloques",
                   "Cada bloque del temario repartido en tests de 100 preguntas."),
    CollectionKind("topics", "Temas", "Tests por temas",
                   "Cada tema repartido en tests de hasta 100 preguntas."),
    CollectionKind("years", "Años", "Tests por años",
                   "Las preguntas de cada año repartidas en tests de 100."),
)}


@dataclass(frozen=True)
class FixedTest:
    title: str
    filters: GeneratorFilters
    questions: int          # preguntas de este test
    block: str | None = None
    topic: str | None = None
    year: int | None = None

    @property
    def source_ref(self) -> str:
        return self.filters.to_source_ref()


def fixed_test_title(f: GeneratorFilters) -> str:
    """Título de un test fijo a partir de sus filtros (también para el historial)."""
    if f.weighted:
        return f"Test Ponderado #{f.part}"
    if f.topic:
        return f"Test Tema {f.topic} #{f.part}"
    if f.block:
        return f"Test Bloque {f.block} #{f.part}"
    if f.year is not None:
        return f"Test {f.year} #{f.part}"
    return f"Test Aleatorio #{f.part}"


def _chunks(base: GeneratorFilters, available: int, **extra) -> list[FixedTest]:
    tests = []
    for part in range(1, math.ceil(available / COLLECTION_SIZE) + 1):
        f = GeneratorFilters(**{**base.__dict__, "count": COLLECTION_SIZE, "part": part})
        n = min(COLLECTION_SIZE, available - (part - 1) * COLLECTION_SIZE)
        tests.append(FixedTest(fixed_test_title(f), f, n, **extra))
    return tests


def build_collection(kind: str, syllabus_id: str, total: int, facets: dict) -> list[FixedTest]:
    """Tests de una colección. ``total``: preguntas del temario; ``facets``: ``generator_facets`` sin filtros."""
    if kind not in KINDS:
        raise ValueError(f"Colección desconocida: {kind}")
    base = GeneratorFilters(syllabus_id)
    if kind == "random":
        return _chunks(base, total)
    if kind == "relevance":
        if not facets.get("weighted"):
            return []  # el temario no tiene preguntas de examen oficial clasificadas por tema
        tests = []
        for part in range(1, RELEVANCE_TESTS + 1):
            f = GeneratorFilters(syllabus_id, weighted=True, count=COLLECTION_SIZE, part=part)
            tests.append(FixedTest(fixed_test_title(f), f, min(COLLECTION_SIZE, total)))
        return tests
    if kind == "blocks":
        return [t for b in facets["blocks"]
                for t in _chunks(GeneratorFilters(syllabus_id, block=b["block"]), b["count"], block=b["block"])]
    if kind == "topics":
        return [t for b in facets["blocks"] for tp in b["topics"]
                for t in _chunks(GeneratorFilters(syllabus_id, block=b["block"], topic=tp["topic"]), tp["count"],
                                 block=b["block"], topic=tp["topic"])]
    return [t for y in facets["years"]
            for t in _chunks(GeneratorFilters(syllabus_id, year=y["year"]), y["count"], year=y["year"])]
