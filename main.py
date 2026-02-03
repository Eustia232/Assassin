from pathlib import Path
from src.settings_store import SettingsStore
from src.reader import ReaderCore


def main():
    project_root = Path(".").resolve()
    settings_path = project_root / "settings.json"
    settings = SettingsStore(settings_path)

    reader = ReaderCore()
    print("Minimal reader CLI for smoke test")
    print("Settings loaded:", settings.get())


if __name__ == "__main__":
    main()
