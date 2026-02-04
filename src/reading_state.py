from pathlib import Path
import json
from typing import Dict, Any, Optional


class ReadingState:
    """Stores and retrieves last reading state (file path, scroll position, chapter index)."""

    def __init__(self, path: Optional[Path] = None):
        project_root = Path(".").resolve()
        self.path = path or (project_root / "reading_state.json")
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self._data = data
            except Exception:
                self._data = {}

    def _atomic_write(self) -> None:
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)

    def save_state(
        self,
        file_path: Optional[Path],
        chapter_index: int = 0,
        scroll_position: int = 0,
    ) -> None:
        """Save current reading state."""
        self._data["last_file"] = str(file_path.resolve()) if file_path else None
        self._data["chapter_index"] = chapter_index
        self._data["scroll_position"] = scroll_position
        try:
            self._atomic_write()
        except Exception:
            pass

    def get_state(self) -> Dict[str, Any]:
        """Get last reading state."""
        return {
            "last_file": self._data.get("last_file"),
            "chapter_index": self._data.get("chapter_index", 0),
            "scroll_position": self._data.get("scroll_position", 0),
        }

    def get_last_file(self) -> Optional[Path]:
        """Get path to last opened file, or None if not set or file doesn't exist."""
        last = self._data.get("last_file")
        if last:
            p = Path(last)
            if p.exists():
                return p
        return None
