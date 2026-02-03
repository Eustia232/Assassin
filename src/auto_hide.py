import threading
import time
from typing import Callable, Optional


class AutoHideController:
    def __init__(self, hide_callback: Callable[[], None], delay_ms: int = 600):
        self.hide_callback = hide_callback
        self.delay_ms = delay_ms
        self._timer: Optional[threading.Timer] = None

    def start_hide_timer(self):
        self.cancel()
        self._timer = threading.Timer(self.delay_ms / 1000.0, self._do_hide)
        self._timer.start()

    def cancel(self):
        if self._timer:
            try:
                self._timer.cancel()
            except Exception:
                pass
            self._timer = None

    def _do_hide(self):
        try:
            self.hide_callback()
        except Exception:
            pass
