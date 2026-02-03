import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.auto_hide import AutoHideController


def test_auto_hide_triggers_callback():
    called = {"v": False}

    def cb():
        called["v"] = True

    ah = AutoHideController(cb, delay_ms=100)
    ah.start_hide_timer()
    time.sleep(0.2)
    assert called["v"] is True
