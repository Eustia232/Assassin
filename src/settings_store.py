from pathlib import Path
import json
import threading
from typing import Dict, Any

DEFAULT_SETTINGS = {
    "font_family": "Noto Sans",
    "font_size": 18,
    "text_color": "#111111",
    "bg_color": "#FFFFFF",
    "auto_hide_enabled": True,
    "auto_hide_delay_ms": 600,
    "hotkey": "Ctrl+Shift+H",
}


class SettingsStore:
    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.Lock()
        self._debounce_timer = None
        self._data = DEFAULT_SETTINGS.copy()
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self._data.update(data)
            except Exception:
                # ignore and keep defaults
                pass

    def get(self) -> Dict[str, Any]:
        return self._data.copy()

    def _atomic_write(self, data: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)

    def save(self, data: Dict[str, Any], debounce_ms: int = 0) -> None:
        def _save_now():
            with self._lock:
                self._data.update(data)
                try:
                    self._atomic_write(self._data)
                except Exception:
                    pass

        if debounce_ms > 0:
            if self._debounce_timer:
                self._debounce_timer.cancel()
            self._debounce_timer = threading.Timer(debounce_ms / 1000.0, _save_now)
            self._debounce_timer.start()
        else:
            _save_now()
