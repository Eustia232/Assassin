from pathlib import Path
import json
import sys
from typing import Dict, Any, List, Optional

from .reader import ReaderCore


def _get_app_dir() -> Path:
    """Get the directory where the application (exe or script) is located."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent


class LibraryStore:
    """A minimal library index stored as JSON. Stores basic metadata for imported books.

    This is intentionally simple: keys are resolved absolute paths as strings.
    """

    def __init__(self, path: Optional[Path] = None):
        app_dir = _get_app_dir()
        self.path = path or (app_dir / "library.json")
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
                # keep empty on error
                self._data = {}

    def _atomic_write(self, data: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)

    def add_book(
        self, file_path: Path, title: Optional[str] = None, author: Optional[str] = None
    ) -> Dict[str, Any]:
        p = Path(file_path).resolve()
        key = str(p)
        # try to auto-detect title using ReaderCore
        if title is None:
            try:
                rc = ReaderCore()
                rc.load_txt(p)
                html = rc.get_current_chapter_html()
                # extract title from the generated html <h2>Title</h2>
                if html.startswith("<h2>"):
                    end = html.find("</h2>")
                    if end != -1:
                        title = html[4:end]
            except Exception:
                title = None
        if not title:
            title = p.stem

        meta = {"title": title, "author": author, "path": key}
        self._data[key] = meta
        try:
            self._atomic_write(self._data)
        except Exception:
            pass
        return meta

    def list_books(self) -> List[Dict[str, Any]]:
        return list(self._data.values())

    def get_book(self, file_path: Path) -> Optional[Dict[str, Any]]:
        key = str(Path(file_path).resolve())
        return self._data.get(key)

    def remove_book(self, file_path: Path) -> None:
        key = str(Path(file_path).resolve())
        if key in self._data:
            del self._data[key]
            try:
                self._atomic_write(self._data)
            except Exception:
                pass
