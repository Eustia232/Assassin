from pathlib import Path
from src.packager import build_exe


def test_build_exe_no_pyinstaller(monkeypatch, tmp_path: Path):
    # If pyinstaller not available, build_exe should return non-zero exit code
    monkeypatch.setattr(
        "subprocess.run", lambda *args, **kwargs: type("R", (), {"returncode": 2})()
    )
    rc = build_exe(tmp_path / "main.py")
    assert rc != 0
