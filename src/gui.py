from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTextBrowser,
    QListWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QSplitter,
    QHBoxLayout,
    QAction,
    QDialog,
    QSystemTrayIcon,
    QMenu,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from .reader import ReaderCore
from .settings_store import SettingsStore
from .settings_controller import SettingsController
from .style import wrap_html_with_style
from .auto_hide import AutoHideController
from .hotkey_manager import HotkeyManager


class QtReaderView:
    def __init__(self, parent: Optional[QWidget] = None):
        self.widget = QTextBrowser(parent)
        self._inner_html = ""

    def set_content(self, inner_html: str) -> None:
        self._inner_html = inner_html
        # Don't render style here; let apply_style do it
        self.widget.setHtml(inner_html)

    def apply_style(self, style) -> None:
        html = wrap_html_with_style(self._inner_html, style)
        self.widget.setHtml(html)


class SettingsDialog(QDialog):
    # Minimal placeholder; real UI is implemented later
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")


class MainWindow(QMainWindow):
    def __init__(self, settings_path: Optional[Path] = None):
        super().__init__()
        self.setWindowTitle("Reader")
        self.resize(900, 600)

        project_root = Path(".").resolve()
        if settings_path is None:
            settings_path = project_root / "settings.json"

        self.settings_store = SettingsStore(settings_path)
        self.reader_core = ReaderCore()
        self.settings_controller = SettingsController(self.settings_store)

        # UI layout
        central = QWidget()
        self.setCentralWidget(central)
        h = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        h.addWidget(splitter)

        # Library list
        self.library_list = QListWidget()
        splitter.addWidget(self.library_list)

        # Reader view
        self.reader_view = QtReaderView()
        splitter.addWidget(self.reader_view.widget)

        # Buttons
        btn_layout = QVBoxLayout()
        self.import_btn = QPushButton("Import")
        self.import_btn.clicked.connect(self.import_file_dialog)
        btn_layout.addWidget(self.import_btn)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)
        btn_layout.addWidget(self.settings_btn)

        btn_layout.addStretch()
        h.addLayout(btn_layout)

        # Tray
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon())
        menu = QMenu()
        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)
        menu.addAction(exit_act)
        self.tray.setContextMenu(menu)
        try:
            self.tray.show()
        except Exception:
            pass

        # Auto-hide and hotkey
        self.auto_hide = AutoHideController(
            self._do_hide,
            delay_ms=self.settings_store.get().get("auto_hide_delay_ms", 600),
        )
        self.hotkey_manager = HotkeyManager()
        hk = self.settings_store.get().get("hotkey")
        if hk:
            ok = self.hotkey_manager.register_hotkey(hk, self._toggle_visibility)
            if not ok:
                # fallback to app-level QShortcut omitted for brevity
                pass

        # Link settings controller to view
        self.settings_controller.set_view(self.reader_view)
        self.settings_controller.apply_settings_to_view()

        # library list activation
        self.library_list.itemActivated.connect(self._on_library_item_activated)

    def import_file_dialog(self) -> None:
        fn, _ = QFileDialog.getOpenFileName(
            self, "Open text file", str(Path(".").resolve()), "Text Files (*.txt)"
        )
        if fn:
            self.open_text_file(Path(fn))

    def open_text_file(self, path: Path) -> None:
        self.reader_core.load_txt(path)
        html = self.reader_core.get_current_chapter_html()
        self.reader_view.set_content(html)
        # ensure style applied
        self.settings_controller.apply_settings_to_view()

    def _on_library_item_activated(self, item):
        path = Path(item.data(Qt.UserRole)) if item.data(Qt.UserRole) else None
        if path:
            self.open_text_file(path)

    def open_settings(self) -> None:
        dlg = SettingsDialog(self)
        dlg.exec()

    def _do_hide(self) -> None:
        try:
            self.hide()
        except Exception:
            pass

    def _toggle_visibility(self) -> None:
        if self.isVisible():
            self.hide()
        else:
            self.show()


def run_app():
    app = QApplication.instance() or QApplication([])
    mw = MainWindow()
    mw.show()
    return app.exec()
