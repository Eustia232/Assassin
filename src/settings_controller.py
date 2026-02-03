from typing import Optional, Any, Dict
from pydantic import ValidationError

from .settings_store import SettingsStore
from .models import StyleSettings


class SettingsController:
    def __init__(
        self, store: SettingsStore, view: Optional[Any] = None, debounce_ms: int = 200
    ):
        self.store = store
        self.view = view
        self.debounce_ms = debounce_ms
        self._settings: Dict[str, Any] = self.store.get()
        # ensure model
        try:
            self._model = StyleSettings(**self._settings)
        except ValidationError:
            self._model = StyleSettings()

    def set_view(self, view: Any) -> None:
        self.view = view

    def set_content(self, inner_html: str) -> None:
        # pass content to view; view is responsible for wrapping with style
        if self.view is not None:
            self.view.set_content(inner_html)

    def apply_settings_to_view(self) -> None:
        if self.view is None:
            return
        self.view.apply_style(self._model)

    def update_setting(self, key: str, value: Any, persist: bool = True) -> None:
        # update in-memory
        self._settings[key] = value
        # revalidate model (guarded)
        try:
            self._model = StyleSettings(**self._settings)
        except ValidationError:
            # ignore invalid updates
            return
        # apply to view immediately for preview
        if self.view is not None:
            self.view.apply_style(self._model)
        # persist
        if persist:
            self.store.save(self._settings, debounce_ms=self.debounce_ms)

    def get_settings(self) -> Dict[str, Any]:
        return self._settings.copy()
