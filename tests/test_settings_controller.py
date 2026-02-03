from pathlib import Path
from src.settings_store import SettingsStore
from src.ui_stub import ReaderViewStub
from src.settings_controller import SettingsController


def test_settings_controller_applies_and_persists(tmp_path: Path):
    p = tmp_path / "settings.json"
    store = SettingsStore(p)
    view = ReaderViewStub()
    ctrl = SettingsController(store, view=view, debounce_ms=0)

    ctrl.set_content("<p>hello</p>")
    ctrl.update_setting("font_size", 22, persist=True)

    # persisted
    s2 = SettingsStore(p)
    assert s2.get()["font_size"] == 22
    # view updated
    rendered = view.get_rendered()
    assert "font-size: 22px" in rendered
