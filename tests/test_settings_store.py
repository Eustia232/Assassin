from pathlib import Path
import tempfile
from src.settings_store import SettingsStore


def test_settings_load_and_save(tmp_path: Path):
    p = tmp_path / "settings.json"
    store = SettingsStore(p)
    # defaults present
    d = store.get()
    assert "font_size" in d

    # save override and reload
    store.save({"font_size": 24}, debounce_ms=0)
    # ensure file written
    assert p.exists()
    new_store = SettingsStore(p)
    assert new_store.get()["font_size"] == 24
