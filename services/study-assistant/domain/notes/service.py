"""Servicio de dominio para la gestión y filtrado de notas."""

import math
import re
import unicodedata
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from domain.notes.models import DashboardMetrics, Note, ProcessSummary


def _normalize_text(text: str) -> str:
    """Elimina acentos y convierte a minúsculas."""
    if not text:
        return ""
    text = str(text).lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

def _natural_sort_key(s: str) -> List[str]:
    """Genera una clave para ordenación natural."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", str(s))]


_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}
# «I.05», «Tema I.05», «TEMA III.01», «II.16.», «I.06.II_Identidad», «B4.03»
_TOPIC_WITH_BLOCK_RE = re.compile(r"(?<![A-Za-z])([IVXL]+|[A-Z]\d+)\.(\d+)(?:\.([IVXL]+|\d+)(?![A-Za-z]))?")
# «Tema 5. Esquema…», «Tema 11. Real Decreto…»
_TOPIC_NUMBER_RE = re.compile(r"\btema\s+(\d+)\b", re.IGNORECASE)
# Respaldo con el id: «tema-i-06-ii-identidad», «cm-ad-ia-p01-tema-006-arquitectura»
_ID_WITH_BLOCK_RE = re.compile(r"(?:^|-)tema-([ivxl]+)-(\d+)(?:-([ivxl]+)(?=-|$))?")
_ID_NUMBER_RE = re.compile(r"(?:^|-)tema-(\d+)(?=-|$)")
_ID_PROFILE_RE = re.compile(r"(?:^|-)p(\d+)(?=-)")


def _roman_to_int(value: str) -> int:
    total, prev = 0, 0
    for ch in reversed(value.upper()):
        n = _ROMAN.get(ch, 0)
        total = total - n if n < prev else total + n
        prev = max(prev, n)
    return total


def _block_key(block: str) -> Tuple[int, int]:
    """Bloques romanos (I, II…) antes que bloques con letra (B4…)."""
    if block[0].upper() in _ROMAN and block.upper().strip("IVXL") == "":
        return (0, _roman_to_int(block))
    return (ord(block[0].upper()), int(block[1:] or 0))


def _subpart_key(sub: Optional[str]) -> int:
    if not sub:
        return 0
    return int(sub) if sub.isdigit() else _roman_to_int(sub)


def parse_topic_position(note: Note) -> Optional[Tuple[Tuple[int, int], int, int]]:
    """(bloque, tema, subparte) a partir del tema oficial o, si no se puede, del id. None si no hay numeración."""
    topic = note.official_topic or ""
    m = _TOPIC_WITH_BLOCK_RE.search(topic)
    if m:
        return _block_key(m.group(1)), int(m.group(2)), _subpart_key(m.group(3))
    m = _TOPIC_NUMBER_RE.search(topic)
    if m:
        return (0, 0), int(m.group(1)), 0
    note_id = (note.id or "").lower()
    m = _ID_WITH_BLOCK_RE.search(note_id)
    if m:
        return _block_key(m.group(1)), int(m.group(2)), _subpart_key(m.group(3))
    m = _ID_NUMBER_RE.search(note_id)
    if m:
        return (0, 0), int(m.group(1)), 0
    return None


def _profile(note: Note) -> int:
    """Perfil del id («cm-ad-tic-p04-tema-…» → 4); 0 si es temario común."""
    m = _ID_PROFILE_RE.search((note.id or "").lower())
    return int(m.group(1)) if m else 0


def sort_by_topic(notes: List[Note]) -> List[Note]:
    """Ordena por bloque, tema y subparte; los apuntes sin numeración van al final, en orden alfabético.

    Los temas de un perfil (p01, p04…) van seguidos y se colocan donde empieza su numeración,
    en vez de intercalarse tema a tema con los de otro perfil: en Comunidad de Madrid cada perfil
    es un temario propio (TIC p01 temas 2-6 y luego p04 temas 2-7; IA comunes 1-3, p01 4-7, p02 4-7, comunes 8-11).
    """
    positions = {id(n): parse_topic_position(n) for n in notes}
    profile_start: Dict[int, tuple] = {}
    for n in notes:
        pos, prof = positions[id(n)], _profile(n)
        if pos is not None and prof and (prof not in profile_start or pos < profile_start[prof]):
            profile_start[prof] = pos

    def key(n: Note) -> tuple:
        pos = positions[id(n)]
        if pos is None:
            return (1, _normalize_text(n.title or n.official_topic or n.id), _natural_sort_key(n.id or ""))
        prof = _profile(n)
        anchor = profile_start.get(prof, pos) if prof else pos
        return (0, anchor, prof, pos, _natural_sort_key(n.id or ""), _natural_sort_key(n.title or ""))

    return sorted(notes, key=key)


class NoteService:
    """Servicio de dominio que implementa la lógica de negocio para las notas."""

    def __init__(self, notes: List[Note]) -> None:
        """Inicializa el servicio con una lista pre-cargada de notas."""
        self.notes = notes
        self._notes_by_id: Dict[str, Note] = {note.id: note for note in notes if note.id}
        self._titles_cache: Dict[str, str] = {}

    def find_by_id(self, note_id: str) -> Optional[Note]:
        """Busca una nota por su identificador con complejidad O(1)."""
        return self._notes_by_id.get(note_id)

    def filter_notes(
        self, query: str = "", tag: str = "", process: str = "", status: str = ""
    ) -> List[Note]:
        """Filtra notas según múltiples criterios."""
        filtered = []
        query_norm = _normalize_text(query).strip() if query else ""
        
        for note in self.notes:
            if status and note.status != status:
                continue
            if tag and tag not in note.tags:
                continue
            if process and process not in note.processes:
                continue
                
            if query_norm:
                search_parts = [
                    note.title,
                    note.official_topic or "",
                    note.excerpt,
                    note.content_text,
                    " ".join(note.tags),
                    " ".join(note.processes),
                ]
                search_blob = _normalize_text(" ".join(search_parts))
                if query_norm not in search_blob:
                    continue
                    
            filtered.append(note)
            
        return filtered

    def get_by_process(self, process_slug: str) -> List[Note]:
        """Obtiene las notas asociadas a un proceso selectivo."""
        if not process_slug:
            return []
        return [note for note in self.notes if process_slug in note.processes]

    def sort_sequentially(self, notes: List[Note]) -> List[Note]:
        """Ordena por bloque/tema/subparte (ver sort_by_topic); sin numeración, al final."""
        return sort_by_topic(notes)

    def collect_unique(self, field: str) -> List[str]:
        """Recolecta valores únicos ordenados de forma natural para un campo específico."""
        values = set()
        for note in self.notes:
            val = getattr(note, field, None)
            if isinstance(val, list):
                for item in val:
                    if item:
                        values.add(str(item))
            elif val:
                values.add(str(val))
        return sorted(list(values), key=_natural_sort_key)

    def collect_statuses(self) -> List[str]:
        """Recolecta estados únicos ordenados alfabéticamente."""
        statuses = {note.status for note in self.notes if note.status}
        return sorted(list(statuses), key=_natural_sort_key)

    def get_dashboard_metrics(self) -> DashboardMetrics:
        """Calcula los indicadores clave de rendimiento (KPIs) para el dashboard."""
        metrics = DashboardMetrics()
        metrics.total_notes = len(self.notes)
        
        processes_set = set()
        reviewed_statuses = {"revisado", "publicado", "completo", "listo"}
        
        proc_counts = defaultdict(lambda: {"total": 0, "reviewed": 0, "draft": 0, "tags": defaultdict(int)})

        for note in self.notes:
            is_reviewed = note.status.lower() in reviewed_statuses
            if is_reviewed:
                metrics.reviewed_count += 1
            else:
                metrics.draft_count += 1
                
            for proc in note.processes:
                processes_set.add(proc)
                p_data = proc_counts[proc]
                p_data["total"] += 1
                if is_reviewed:
                    p_data["reviewed"] += 1
                else:
                    p_data["draft"] += 1
                    
                for tag in note.tags:
                    p_data["tags"][tag] += 1
                    
        metrics.total_processes = len(processes_set)
        
        for slug in processes_set:
            p_data = proc_counts[slug]
            sorted_tags = sorted(p_data["tags"].items(), key=lambda x: x[1], reverse=True)
            top_tags = [t[0] for t in sorted_tags[:3]]
            
            summary = ProcessSummary(
                slug=slug,
                title=self.format_process_title(slug),
                total=p_data["total"],
                reviewed=p_data["reviewed"],
                draft=p_data["draft"],
                top_tags=top_tags
            )
            metrics.process_summaries.append(summary)
            
        metrics.process_summaries.sort(key=lambda s: s.title)
        return metrics

    def get_adjacent_notes(self, note: Note, process: Optional[str] = None) -> Tuple[Optional[Note], Optional[Note]]:
        """Devuelve la nota anterior y siguiente en orden secuencial (opcionalmente dentro de un proceso)."""
        if process:
            candidates = self.get_by_process(process)
        else:
            candidates = self.notes.copy()
            
        sorted_notes = self.sort_sequentially(candidates)
        
        try:
            idx = next(i for i, n in enumerate(sorted_notes) if n.id == note.id)
            prev_note = sorted_notes[idx - 1] if idx > 0 else None
            next_note = sorted_notes[idx + 1] if idx < len(sorted_notes) - 1 else None
            return prev_note, next_note
        except StopIteration:
            return None, None

    def format_process_title(self, slug: str) -> str:
        """Da formato a un slug de proceso para hacerlo legible."""
        if not slug or slug.lower() == "sin proceso":
            return "Sin proceso asignado"
            
        if slug in self._titles_cache:
            return self._titles_cache[slug]
            
        segments = slug.split("/")
        formatted_segments = []
        connectors = {"de", "del", "la", "las", "el", "los", "en", "y", "a", "por", "para", "con", "e"}
        accents = {
            "administracion": "Administración",
            "innovacion": "Innovación",
            "transformacion": "Transformación",
            "informatica": "Informática",
            "gestion": "Gestión",
            "tecnico": "Técnico",
            "comunicacion": "Comunicación",
        }

        for segment in segments:
            words = re.split(r"[\s\-_]+", segment.strip())
            formatted_words = []
            
            for i, word in enumerate(words):
                lower = word.lower()
                if not lower:
                    continue
                    
                if lower in accents:
                    formatted_words.append(accents[lower])
                elif i > 0 and lower in connectors:
                    formatted_words.append(lower)
                elif len(lower) <= 3 or re.match(r"^[a-z][0-9]$", lower, re.IGNORECASE):
                    formatted_words.append(lower.upper())
                else:
                    formatted_words.append(lower.capitalize())
                    
            if formatted_words:
                formatted_segments.append(" ".join(formatted_words))
                
        formatted = " › ".join(formatted_segments) if formatted_segments else slug
        self._titles_cache[slug] = formatted
        return formatted

    def estimate_reading_time(self, note: Note) -> str:
        """Estima el tiempo de lectura basándose en la cantidad de caracteres."""
        text = note.content_text or note.excerpt or ""
        char_count = len(text)
        minutes = max(1, math.ceil(char_count / 800))
        return f"~{minutes} min"

    def extract_practice_topics(self, note: Note) -> List[str]:
        """Extrae los temas de práctica normalizados de una nota."""
        practice_topics = []
        
        topics = note.practice.get("topics", [])
        if isinstance(topics, list):
            for topic in topics:
                t = str(topic).strip()
                if t:
                    practice_topics.append(t)
                    
        if not practice_topics and note.tags:
            for tag in note.tags:
                t = str(tag).strip()
                if t:
                    practice_topics.append(t)
                    
        if not practice_topics and note.official_topic:
            match = re.search(r"Tema\s+([0-9]+)", note.official_topic, re.IGNORECASE)
            if match:
                practice_topics.append(match.group(1).strip())
            else:
                practice_topics.append(note.official_topic.strip())
                
        seen = set()
        result = []
        for t in practice_topics:
            if t not in seen and t:
                seen.add(t)
                result.append(t)
                
        return result
