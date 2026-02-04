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
    QSlider,
)
from PySide6.QtGui import (
    QIcon,
    QAction,
    QColor,
    QCursor,
    QShortcut,
    QKeySequence,
    QPainter,
    QBrush,
)
from PySide6.QtCore import Qt, QTimer, QPoint

from .reader import ReaderCore
from .settings_store import SettingsStore
from .settings_controller import SettingsController
from .style import wrap_html_with_style
from .hotkey_manager import HotkeyManager
from .reading_state import ReadingState


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

        # Window opacity slider (1-100)
        opacity_layout = QHBoxLayout()
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(1, 100)
        self.opacity_slider.setValue(self._current_settings.get("window_opacity", 100))
        self.opacity_slider.valueChanged.connect(self._on_opacity_changed)
        opacity_layout.addWidget(self.opacity_slider)
        self.opacity_label = QLabel(f"{self.opacity_slider.value()}%")
        self.opacity_label.setMinimumWidth(40)
        opacity_layout.addWidget(self.opacity_label)
        form.addRow("Window Opacity:", opacity_layout)

        # Hotkey
        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setText(self._current_settings.get("hotkey", "Ctrl+Shift+H"))
        self.hotkey_edit.textChanged.connect(self._on_hotkey_changed)
        form.addRow("Hotkey:", self.hotkey_edit)

        # Auto-hide on mouse leave checkbox
        self.auto_hide_checkbox = QCheckBox("Hide window when mouse leaves")
        self.auto_hide_checkbox.setChecked(
            self._current_settings.get("auto_hide_enabled", False)
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

    def _on_opacity_changed(self, value):
        self._current_settings["window_opacity"] = value
        self.opacity_label.setText(f"{value}%")
        # Apply immediately for live preview
        if self.parent() and hasattr(self.parent(), "set_window_opacity"):
            self.parent().set_window_opacity(value)

    def _on_hotkey_changed(self, text):
        self._current_settings["hotkey"] = text

    def _on_auto_hide_changed(self, state):
        self._current_settings["auto_hide_enabled"] = state == Qt.Checked.value

    def accept(self):
        # Persist all settings on OK
        for key, value in self._current_settings.items():
            self.settings_controller.update_setting(key, value, persist=True)
        super().accept()

    def reject(self):
        # Revert opacity change
        original = self.settings_controller.get_settings()
        if self.parent() and hasattr(self.parent(), "set_window_opacity"):
            self.parent().set_window_opacity(original.get("window_opacity", 100))
        self.settings_controller.apply_settings_to_view()
        super().reject()


class TransparentFrame(QWidget):
    """A widget that draws a semi-transparent background."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._opacity = 1.0  # 0.0 to 1.0
        self._bg_color = QColor(255, 255, 255)
        self._text_browser: Optional[QTextBrowser] = None

    def set_text_browser(self, browser: QTextBrowser) -> None:
        """Set the text browser to forward wheel events to."""
        self._text_browser = browser

    def set_opacity(self, opacity: float) -> None:
        self._opacity = max(0.005, min(1.0, opacity))
        self.repaint()

    def set_bg_color(self, color: QColor) -> None:
        self._bg_color = color
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        color = QColor(self._bg_color)
        color.setAlphaF(self._opacity)
        painter.fillRect(self.rect(), QBrush(color))

    def wheelEvent(self, event) -> None:
        """Forward wheel events to the text browser for scrolling."""
        if self._text_browser:
            # Forward the event to the text browser's viewport
            self._text_browser.wheelEvent(event)
        else:
            super().wheelEvent(event)


class TitleBar(QWidget):
    """Simple custom title bar for frameless window."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self._drag_pos: Optional[QPoint] = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(5)

        self.title_label = QLabel("Reader")
        self.title_label.setStyleSheet("font-weight: bold; color: #333;")
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Minimize button
        self.min_btn = QPushButton("─")
        self.min_btn.setFixedSize(30, 24)
        self.min_btn.setStyleSheet(
            "QPushButton { border: none; background: transparent; } "
            "QPushButton:hover { background: #ddd; }"
        )
        self.min_btn.clicked.connect(lambda: self.window().showMinimized())
        layout.addWidget(self.min_btn)

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 24)
        self.close_btn.setStyleSheet(
            "QPushButton { border: none; background: transparent; font-size: 16px; } "
            "QPushButton:hover { background: #e81123; color: white; }"
        )
        self.close_btn.clicked.connect(lambda: self.window().close())
        layout.addWidget(self.close_btn)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos is not None and event.buttons() == Qt.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None


class MainWindow(QMainWindow):
    def __init__(self, settings_path: Optional[Path] = None):
        super().__init__()
        self.setWindowTitle("Reader")
        self.resize(900, 600)
        self.setMouseTracking(True)

        # Frameless window with transparent background
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        project_root = Path(".").resolve()
        if settings_path is None:
            settings_path = project_root / "settings.json"

        self.settings_store = SettingsStore(settings_path)
        self.reading_state = ReadingState(project_root / "reading_state.json")
        self.reader_core = ReaderCore()
        self.settings_controller = SettingsController(self.settings_store)
        self._current_file: Optional[Path] = None  # Track currently opened file

        # Reset auto-hide and opacity on each startup
        self.settings_store.save(
            {"auto_hide_enabled": False, "window_opacity": 100}, debounce_ms=0
        )

        # Transparent frame as central widget
        self._frame = TransparentFrame()
        self._frame.setMouseTracking(True)
        self.setCentralWidget(self._frame)

        # Main layout
        main_layout = QVBoxLayout(self._frame)
        main_layout.setContentsMargins(1, 1, 1, 1)  # Thin border
        main_layout.setSpacing(0)

        # Custom title bar
        self._title_bar = TitleBar()
        main_layout.addWidget(self._title_bar)

        # Reader view (main content area)
        self.reader_view = QtReaderView()
        self.reader_view.widget.setMouseTracking(True)
        # Hide scrollbars but keep scrolling enabled
        self.reader_view.widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.reader_view.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Make text browser background transparent, ensure viewport is also transparent
        self.reader_view.widget.setStyleSheet(
            "QTextBrowser { background: transparent; border: none; }"
            "QTextBrowser > QWidget { background: transparent; }"
        )
        # Ensure the viewport is transparent
        viewport = self.reader_view.widget.viewport()
        if viewport:
            viewport.setAutoFillBackground(False)
        main_layout.addWidget(self.reader_view.widget, stretch=1)

        # Connect text browser to frame for wheel event forwarding
        self._frame.set_text_browser(self.reader_view.widget)

        # Keyboard shortcuts (Ctrl+O for Import, Ctrl+P for Settings)
        self._shortcut_import = QShortcut(QKeySequence("Ctrl+O"), self)
        self._shortcut_import.activated.connect(self.import_file_dialog)

        self._shortcut_settings = QShortcut(QKeySequence("Ctrl+P"), self)
        self._shortcut_settings.activated.connect(self.open_settings)

        # Apply window opacity (100% on startup)
        self.setWindowOpacity(1.0)

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

        # Auto-hide using QTimer (thread-safe for Qt)
        self._auto_hide_timer = QTimer(self)
        self._auto_hide_timer.setSingleShot(True)
        self._auto_hide_timer.timeout.connect(self._do_hide)
        self._dialog_open = False  # Flag to prevent auto-hide when dialogs are open

        # Mouse tracking timer - checks if mouse is outside window bounds
        self._mouse_check_timer = QTimer(self)
        self._mouse_check_timer.setInterval(100)  # Check every 100ms
        self._mouse_check_timer.timeout.connect(self._check_mouse_position)
        self._mouse_check_timer.start()

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

        # Restore last reading state
        self._restore_reading_state()

    def set_window_opacity(self, opacity_percent: int) -> None:
        """Set window background opacity (0-100). Text remains opaque."""
        opacity_percent = max(0, min(100, opacity_percent))
        opacity = opacity_percent / 100.0
        self._frame.set_opacity(opacity)

    def _check_mouse_position(self) -> None:
        """Check if mouse is outside the entire window (including title bar)."""
        # Don't auto-hide if disabled, dialog is open, or window is hidden
        if self._dialog_open or not self.isVisible():
            return
        if not self.settings_store.get().get("auto_hide_enabled", False):
            return

        # Get global mouse position and window geometry
        cursor_pos = QCursor.pos()  # Global mouse position
        window_rect = self.frameGeometry()  # Includes title bar

        # If mouse is outside window bounds, hide immediately
        if not window_rect.contains(cursor_pos):
            self.hide()

    def import_file_dialog(self) -> None:
        # Prevent auto-hide while dialog is open
        self._dialog_open = True
        self._auto_hide_timer.stop()
        fn, _ = QFileDialog.getOpenFileName(
            self, "Open text file", str(Path(".").resolve()), "Text Files (*.txt)"
        )
        self._dialog_open = False
        if fn:
            self.open_text_file(Path(fn))

    def open_text_file(self, path: Path) -> None:
        self._current_file = path
        self.reader_core.load_txt(path)
        html = self.reader_core.get_current_chapter_html()
        self.reader_view.set_content(html)
        # Update title bar
        self._title_bar.title_label.setText(f"Reader - {path.name}")
        # ensure style applied
        self.settings_controller.apply_settings_to_view()

    def _restore_reading_state(self) -> None:
        """Restore last opened file and scroll position on startup."""
        state = self.reading_state.get_state()
        last_file = self.reading_state.get_last_file()
        if last_file:
            try:
                self.open_text_file(last_file)
                # Restore scroll position after content is loaded
                # Use QTimer to delay until content is rendered
                scroll_pos = state.get("scroll_position", 0)
                if scroll_pos > 0:
                    QTimer.singleShot(
                        100, lambda: self._set_scroll_position(scroll_pos)
                    )
            except Exception:
                pass  # File might be corrupted or inaccessible

    def _set_scroll_position(self, pos: int) -> None:
        """Set scroll position (called after content is rendered)."""
        scrollbar = self.reader_view.widget.verticalScrollBar()
        scrollbar.setValue(pos)

    def _save_reading_state(self) -> None:
        """Save current reading state."""
        scroll_pos = self.reader_view.widget.verticalScrollBar().value()
        chapter_idx = self.reader_core.current_index if self.reader_core.chapters else 0
        self.reading_state.save_state(
            file_path=self._current_file,
            chapter_index=chapter_idx,
            scroll_position=scroll_pos,
        )

    def closeEvent(self, event):
        """Save reading state when window is closed."""
        self._save_reading_state()
        super().closeEvent(event)

    def open_settings(self) -> None:
        # Prevent auto-hide while dialog is open
        self._dialog_open = True
        self._auto_hide_timer.stop()
        dlg = SettingsDialog(self.settings_controller, self)
        dlg.exec()
        self._dialog_open = False
        # Re-apply opacity after dialog closes (in case it was changed and saved)
        opacity = self.settings_store.get().get("window_opacity", 100)
        self.set_window_opacity(opacity)

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
