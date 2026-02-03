import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.hotkey_manager import HotkeyManager


def test_register_hotkey_returns_bool(monkeypatch):
    """Registering a hotkey should return a boolean and not raise.

    The environment may or may not have the `keyboard` module installed; accept
    either True (registered) or False (could not register).
    """
    hk = HotkeyManager()
    result = hk.register_hotkey("ctrl+shift+h", lambda: None)
    assert isinstance(result, bool)
    try:
        hk.unregister_all()
    except Exception:
        pass
