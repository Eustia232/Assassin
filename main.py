import sys
from pathlib import Path
import sys
from src.settings_store import SettingsStore
from src.reader import ReaderCore


def get_app_dir() -> Path:
    """Get the directory where the application (exe or script) is located."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent


def main():
    """Legacy CLI entrypoint kept for compatibility.

    Prefer using `uv run python -c "from src.gui import run_app; run_app()"` to launch
    the GUI. For CI and headless runs this function will print a small smoke
    test summary.
    """
    app_dir = get_app_dir()
    settings_path = app_dir / "settings.json"
    settings = SettingsStore(settings_path)

    reader = ReaderCore()
    print("Minimal reader CLI for smoke test")
    print("Settings loaded:", settings.get())


if __name__ == "__main__":
    # Default behaviour for `uv run main.py` — if the environment allows a
    # GUI we try to start it; otherwise we fall back to the CLI smoke test.
    try:
        # import here to avoid requiring PySide6 in non-GUI runs/tests
        from src.gui import run_app

        # Attempt to run GUI; if it fails because there is no display or
        # PySide6 isn't available we'll catch and fall back.
        rc = run_app()
        # run_app returns exit code from QApplication.exec(); forward it if
        # provided. If it returns None, keep default behaviour.
        if isinstance(rc, int):
            sys.exit(rc)
    except Exception:
        # Fall back to the minimal CLI smoke test
        main()
