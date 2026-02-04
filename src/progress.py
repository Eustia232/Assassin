from pathlib import Path
import json
import sys
from typing import Dict, Any, Optional


def _get_app_dir() -> Path:
    """Get the directory where the application (exe or script) is located."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent


class ProgressStore:
    """Simple per-book progress persistence using JSON per project.

    Stores a dict keyed by absolute path of book file -> {chapter_index, char_offset, bookmarks: []}
    """

    def __init__(self, path: Optional[Path] = None):
        app_dir = _get_app_dir()
        self.path = path or (app_dir / "progress.json")
        self._data: Dict[str, Dict[str, Any]] = {}
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

    def save_progress(
        self, book_path: Path, chapter_index: int, char_offset: int
    ) -> None:
        key = str(Path(book_path).resolve())
        self._data.setdefault(key, {})
        self._data[key]["chapter_index"] = int(chapter_index)
        self._data[key]["char_offset"] = int(char_offset)
        try:
            self._atomic_write()
        except Exception:
            pass

    def add_bookmark(self, book_path: Path, offset: int, note: str = "") -> None:
        key = str(Path(book_path).resolve())
        rec = self._data.setdefault(key, {})
        rec.setdefault("bookmarks", [])
        rec["bookmarks"].append({"offset": int(offset), "note": note})
        try:
            self._atomic_write()
        except Exception:
            pass

    def get_progress(self, book_path: Path) -> Dict[str, Any]:
        return self._data.get(str(Path(book_path).resolve()), {})
