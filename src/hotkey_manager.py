from typing import Callable, Optional
import threading

try:
    import keyboard  # type: ignore
except Exception:
    keyboard = None


class HotkeyManager:
    def __init__(self):
        self._registered = False
        self._callback: Optional[Callable[[], None]] = None
        self._listener_thread: Optional[threading.Thread] = None

    def register_hotkey(self, hotkey: str, callback: Callable[[], None]) -> bool:
        self._callback = callback
        # Try to import keyboard dynamically in case tests monkeypatch sys.modules
        if keyboard is None:
            try:
                import importlib

                kb = importlib.import_module("keyboard")
            except Exception:
                return False
            else:
                globals()["keyboard"] = kb
        try:
            keyboard.add_hotkey(hotkey, callback)
            self._registered = True
            return True
        except Exception:
            return False

    def unregister_all(self) -> None:
        if keyboard is None:
            try:
                import importlib

                kb = importlib.import_module("keyboard")
            except Exception:
                return
            else:
                globals()["keyboard"] = kb
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        self._registered = False
