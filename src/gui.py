from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTextBrowser,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QDialog,
    QSystemTrayIcon,
    QMenu,
    QLabel,
    QSpinBox,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QDialogButtonBox,
    QColorDialog,
    QCheckBox,
)
from PySide6.QtGui import QIcon, QAction, QColor
from PySide6.QtCore import Qt, QEvent

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
    """Settings dialog with font, size, colors, and hotkey controls."""

    def __init__(self, settings_controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.settings_controller = settings_controller
        self._current_settings = settings_controller.get_settings().copy()

        layout = QVBoxLayout(self)

        # Form layout for settings
        form = QFormLayout()

        # Font family
        self.font_combo = QComboBox()
        self.font_combo.addItems(
            ["Noto Sans", "Microsoft YaHei", "SimSun", "Arial", "Times New Roman"]
        )
        self.font_combo.setCurrentText(
            self._current_settings.get("font_family", "Noto Sans")
        )
        self.font_combo.currentTextChanged.connect(self._on_font_changed)
        form.addRow("Font:", self.font_combo)

        # Font size
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(self._current_settings.get("font_size", 18))
        self.size_spin.valueChanged.connect(self._on_size_changed)
        form.addRow("Size:", self.size_spin)

        # Text color
        self.text_color_btn = QPushButton()
        self._text_color = self._current_settings.get("text_color", "#111111")
        self._update_color_button(self.text_color_btn, self._text_color)
        self.text_color_btn.clicked.connect(self._pick_text_color)
        form.addRow("Text Color:", self.text_color_btn)

        # Background color
        self.bg_color_btn = QPushButton()
        self._bg_color = self._current_settings.get("bg_color", "#FFFFFF")
        self._update_color_button(self.bg_color_btn, self._bg_color)
        self.bg_color_btn.clicked.connect(self._pick_bg_color)
        form.addRow("Background:", self.bg_color_btn)

        # Hotkey
        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setText(self._current_settings.get("hotkey", "Ctrl+Shift+H"))
        self.hotkey_edit.textChanged.connect(self._on_hotkey_changed)
        form.addRow("Hotkey:", self.hotkey_edit)

        # Auto-hide delay
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(100, 5000)
        self.delay_spin.setSuffix(" ms")
        self.delay_spin.setValue(self._current_settings.get("auto_hide_delay_ms", 600))
        self.delay_spin.valueChanged.connect(self._on_delay_changed)
        form.addRow("Auto-hide Delay:", self.delay_spin)

        # Auto-hide on mouse leave checkbox
        self.auto_hide_checkbox = QCheckBox("Hide window when mouse leaves")
        self.auto_hide_checkbox.setChecked(
            self._current_settings.get("auto_hide_enabled", True)
        )
        self.auto_hide_checkbox.stateChanged.connect(self._on_auto_hide_changed)
        form.addRow("Auto-hide:", self.auto_hide_checkbox)

        layout.addLayout(form)

        # Preview area
        preview_label = QLabel("Preview:")
        layout.addWidget(preview_label)
        self.preview = QTextBrowser()
        self.preview.setMaximumHeight(100)
        self._update_preview()
        layout.addWidget(self.preview)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _update_color_button(self, btn, color):
        btn.setStyleSheet(f"background-color: {color}; min-width: 60px;")
        btn.setText(color)

    def _update_preview(self):
        from .style import wrap_html_with_style

        html = wrap_html_with_style(
            "<p>Sample text 示例文字</p>", self._current_settings
        )
        self.preview.setHtml(html)

    def _on_font_changed(self, font):
        self._current_settings["font_family"] = font
        self.settings_controller.update_setting("font_family", font, persist=False)
        self._update_preview()

    def _on_size_changed(self, size):
        self._current_settings["font_size"] = size
        self.settings_controller.update_setting("font_size", size, persist=False)
        self._update_preview()

    def _pick_text_color(self):
        color = QColorDialog.getColor(QColor(self._text_color), self)
        if color.isValid():
            self._text_color = color.name()
            self._current_settings["text_color"] = self._text_color
            self._update_color_button(self.text_color_btn, self._text_color)
            self.settings_controller.update_setting(
                "text_color", self._text_color, persist=False
            )
            self._update_preview()

    def _pick_bg_color(self):
        color = QColorDialog.getColor(QColor(self._bg_color), self)
        if color.isValid():
            self._bg_color = color.name()
            self._current_settings["bg_color"] = self._bg_color
            self._update_color_button(self.bg_color_btn, self._bg_color)
            self.settings_controller.update_setting(
                "bg_color", self._bg_color, persist=False
            )
            self._update_preview()

    def _on_hotkey_changed(self, text):
        self._current_settings["hotkey"] = text

    def _on_delay_changed(self, value):
        self._current_settings["auto_hide_delay_ms"] = value

    def _on_auto_hide_changed(self, state):
        self._current_settings["auto_hide_enabled"] = state == Qt.Checked.value

    def accept(self):
        # Persist all settings on OK
        for key, value in self._current_settings.items():
            self.settings_controller.update_setting(key, value, persist=True)
        super().accept()

    def reject(self):
        # Revert preview changes
        original = self.settings_controller.get_settings()
        self.settings_controller.apply_settings_to_view()
        super().reject()


class MainWindow(QMainWindow):
    def __init__(self, settings_path: Optional[Path] = None):
        super().__init__()
        self.setWindowTitle("Reader")
        self.resize(900, 600)
        self.setMouseTracking(True)

        project_root = Path(".").resolve()
        if settings_path is None:
            settings_path = project_root / "settings.json"

        self.settings_store = SettingsStore(settings_path)
        self.reader_core = ReaderCore()
        self.settings_controller = SettingsController(self.settings_store)

        # UI layout
        central = QWidget()
        central.setMouseTracking(True)
        self.setCentralWidget(central)
        h = QHBoxLayout(central)

        # Reader view (main content area, takes most space)
        self.reader_view = QtReaderView()
        self.reader_view.widget.setMouseTracking(True)
        h.addWidget(self.reader_view.widget, stretch=1)

        # Buttons (right side)
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
        menu = QMenu(self)
        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)
        menu.addAction(exit_act)
        self.tray.setContextMenu(menu)
        try:
            self.tray.show()
        except Exception:
            pass

        # Auto-hide controller
        self.auto_hide = AutoHideController(
            self._do_hide,
            delay_ms=self.settings_store.get().get("auto_hide_delay_ms", 600),
        )

        # Hotkey manager
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

    def leaveEvent(self, event):
        """Called when mouse leaves the window."""
        super().leaveEvent(event)
        # Check if auto-hide is enabled
        if self.settings_store.get().get("auto_hide_enabled", True):
            self.auto_hide.start_hide_timer()

    def enterEvent(self, event):
        """Called when mouse enters the window."""
        super().enterEvent(event)
        # Cancel any pending hide timer
        self.auto_hide.cancel()

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

    def open_settings(self) -> None:
        dlg = SettingsDialog(self.settings_controller, self)
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
