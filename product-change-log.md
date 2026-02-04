2026-02-04

- refactor: replace Import/Settings buttons with keyboard shortcuts
  - Removed buttons from main window for cleaner UI
  - Ctrl+O: Open file (Import)
  - Ctrl+P: Open Settings
- fix: text area background now transparent (only text is opaque)
  - Modified `style.py` to set body background to transparent
  - Modified `gui.py` QTextBrowser to have transparent background
  - Window opacity slider now affects entire window uniformly, text remains readable
- feat: frameless transparent window with adjustable opacity (0-100%)
  - Added custom title bar with close/minimize/maximize buttons and drag support
  - Window background opacity adjustable via Settings slider, text always remains opaque
  - Added `TransparentContainer` widget for semi-transparent background rendering
  - Added `window_opacity` setting to settings_store defaults
- fix: auto-hide now detects mouse leaving entire window (including title bar)
  - Changed from `leaveEvent` to polling with `frameGeometry()` which includes window frame
  - Users can now access close/minimize buttons without triggering auto-hide
- feat: add reading state persistence (last file + scroll position)
  - Added: `src/reading_state.py`, `tests/test_reading_state.py`
  - Modified: `src/gui.py` (restore state on startup, save on close)
  - Notes: App now remembers last opened file and scroll position across sessions.
- fix: add pytest pythonpath config to pyproject.toml for test imports
- fix: prevent auto-hide during dialogs with flag, hide immediately on mouse leave (no delay)
- fix: stop auto-hide timer when opening dialogs to prevent crash
- fix: use QTimer for auto-hide instead of threading.Timer (thread-safe for Qt GUI)
- fix: improve encoding detection using charset_normalizer with GBK/GB2312 fallback
- feat: add auto-hide on mouse leave feature with checkbox toggle in Settings
- fix: remove library list splitter, show only single reader view area
- fix: implement SettingsDialog with real controls (font, size, colors, hotkey, auto-hide delay) and live preview
- fix: move QAction import from QtWidgets to QtGui for PySide6 6.x compatibility
- feat: implement library, progress, search index, packaging smoke tests; update docs & TODO
  - Added: `src/library.py`, `src/progress.py`, `src/search_index.py`
  - Added tests: `tests/test_library_store.py`, `tests/test_progress_store.py`, `tests/test_search_index.py`, `tests/test_packaging_smoke.py`
  - Updated: `TODO.md` (marked items 13-20 completed), `README.md`
  - Notes: Implemented minimal LibraryStore, ProgressStore, simple FTS5 search index, packaging smoke test; all tests passing locally (13 passed).

2026-02-03

- feat: scaffold reader application and implement core pieces
  - Added: `src/models.py`, `src/parser.py`, `src/settings_store.py`, `src/reader.py`
  - Added: `main.py`, `tests/test_parser.py`, `TODO.md` (marked first 5 items done), `project.md`
  - Notes: basic chapter parsing, pydantic models, settings atomic write + debounce, simple HTML rendering for chapters.

2026-02-03

- feat: implement GUI backend and integration pieces
  - Added: `src/gui.py`, `src/style.py`, `src/ui_stub.py`, `src/settings_controller.py`, `src/auto_hide.py`, `src/hotkey_manager.py`, `src/packager.py`
  - Added tests for settings controller, hotkey manager, auto-hide, integration load/render, packaging helper
  - Notes: GUI is implemented with minimal features (import, reader view, settings dialog placeholder, system tray). Hotkey integration uses `keyboard` if available; auto-hide uses timer-based controller.
