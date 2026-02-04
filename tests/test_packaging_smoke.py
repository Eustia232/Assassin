from src.packager import build_exe


def test_packaging_smoke():
    # ensure build_exe returns int (already covered), keep smoke test for packaging step
    rc = build_exe("main.py")
    assert isinstance(rc, int)
