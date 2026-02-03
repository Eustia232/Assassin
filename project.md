Project: Windows-only Reader — Tech Stack & Dev Commands

Target
- Platform: Windows 10/11 (Windows-only)
- Python: 3.12+ (managed with `uv`)

Core stack (minimal)
- GUI: `PySide6` (Qt) — rendering, system tray, window/events
- Encoding detection: `charset-normalizer`
- Global hotkey (Windows): `keyboard` (fallback to app-only Qt shortcut if OS/global registration fails)
- Persistence: `settings.json` in project root (global settings only)
- Optional: `pydantic` (models/validation), `pyinstaller` (packaging)

Development commands (using uv)
- Add a dependency: `uv add <package>` (example: `uv add pyside6`)
- Sync/update environment/lock: `uv sync` (if needed)
- Run app or scripts: `uv run python main.py` or `uv run main.py` (project entry)
- Run tests: `uv run pytest`

File & config notes
- Settings file: project root `settings.json` (global only)
- Atomic write: write to temp file then replace to avoid corruption
- Defaults: hotkey `Ctrl+Shift+H`, auto-hide delay 600 ms, font-size range 10–48

Packaging
- Use `pyinstaller` to build a Windows executable: `uv add pyinstaller` then `uv run pyinstaller --onefile main.py`

MVP features (reminder)
- Import `.txt` files; simple chapter split; render HTML/CSS in reader; font/color/size settings with realtime preview; mouse-leave auto-hide + hotkey restore; settings persisted to `settings.json`.
