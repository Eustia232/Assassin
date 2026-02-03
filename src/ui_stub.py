"""A minimal Qt UI stub to wire style application during development and tests.

This module intentionally keeps imports local to avoid requiring PySide6
at test/runtime time. The real UI will live here later.
"""

from typing import Optional
from .models import StyleSettings
from .style import wrap_html_with_style


class ReaderViewStub:
    def __init__(self):
        self._html = ""
        self._style = StyleSettings()

    def apply_style(self, style: StyleSettings):
        self._style = style
        # In the real UI this would call setHtml on a QTextBrowser
        # Here we just render the HTML string for tests
        # assume self._html contains inner content
        self._rendered = wrap_html_with_style(self._html, style)

    def set_content(self, inner_html: str):
        self._html = inner_html
        # reapply style
        self.apply_style(self._style)

    def get_rendered(self) -> str:
        return getattr(self, "_rendered", "")
