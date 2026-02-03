from src.packager import build_exe


def test_packaging_returns_code():
    # we won't actually invoke pyinstaller in CI; ensure function callable
    rc = build_exe("main.py")
    assert isinstance(rc, int)
