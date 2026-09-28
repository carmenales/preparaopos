"""Repositorio de acceso a la base de conocimiento."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from config import KNOWLEDGE_BASE_PATH, KNOWLEDGE_INDEX_PATH
from domain.notes.models import Note


class NoteRepository:
    """Repositorio para acceder a las notas desde el sistema de archivos."""

    def __init__(
        self,
        index_path: Optional[Path] = None,
        knowledge_base_path: Optional[Path] = None,
    ) -> None:
        """Inicializa el repositorio y la caché en memoria."""
        self._index_path: Path = Path(index_path) if index_path else KNOWLEDGE_INDEX_PATH
        self._knowledge_base_path: Path = Path(knowledge_base_path) if knowledge_base_path else KNOWLEDGE_BASE_PATH
        self._notes_cache: List[Note] = []
        self._notes_by_id: Dict[str, Note] = {}
        self._is_loaded: bool = False

    def _load_if_needed(self) -> None:
        """Carga el índice JSON si no se ha cargado previamente."""
        if self._is_loaded:
            return

        if not self._index_path.is_file():
            self._is_loaded = True
            return

        with open(self._index_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        notes_data = data.get("notes", [])
        for note_dict in notes_data:
            note = Note.from_dict(note_dict)
            self._notes_cache.append(note)
            if note.id:
                self._notes_by_id[note.id] = note
                
        self._is_loaded = True

    def get_all(self) -> List[Note]:
        """Devuelve todas las notas."""
        self._load_if_needed()
        return self._notes_cache

    def find_by_id(self, note_id: str) -> Optional[Note]:
        """Encuentra una nota por su identificador único."""
        self._load_if_needed()
        return self._notes_by_id.get(note_id)

    def get_absolute_path(self, note: Note) -> Optional[Path]:
        """Obtiene y valida la ruta absoluta del fichero de la nota."""
        if not note.path:
            return None

        candidate = Path(note.path)

        if not candidate.is_absolute():
            parts = candidate.parts
            if parts and parts[0] == "knowledge":
                candidate = self._knowledge_base_path / Path(*parts[1:])
            else:
                candidate = self._knowledge_base_path / candidate
        
        try:
            resolved = candidate.resolve(strict=False)
        except Exception:
            return None

        if not str(resolved).startswith(str(self._knowledge_base_path.resolve(strict=False))):
            return None

        if resolved.is_file():
            return resolved

        return None

    def read_note_content(self, note: Note) -> str:
        """Lee el contenido Markdown del archivo en disco."""
        path = self.get_absolute_path(note)
        if not path or not path.is_file():
            return ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def resolve_asset_path(self, note_id: str, relative_path: str) -> Optional[Path]:
        """
        Resuelve y valida la ruta absoluta de un asset (imagen).
        
        Asegura que el asset está dentro del directorio de la nota y 
        es de un tipo permitido para evitar Path Traversal.
        """
        note = self.find_by_id(note_id)
        if not note:
            return None
            
        note_path = self.get_absolute_path(note)
        if not note_path:
            return None
            
        note_dir = note_path.parent
        asset_candidate = (note_dir / relative_path).resolve(strict=False)
        
        if not str(asset_candidate).startswith(str(self._knowledge_base_path.resolve(strict=False))):
            return None
            
        allowed_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
        if asset_candidate.suffix.lower() not in allowed_extensions:
            return None
            
        if asset_candidate.is_file():
            return asset_candidate
            
        return None

    def load_index(self) -> List[Note]:
        """Alias de get_all() para compatibilidad con la interfaz esperada."""
        return self.get_all()


# Alias para compatibilidad con imports que esperan el nombre DDD
KnowledgeFSRepository = NoteRepository
