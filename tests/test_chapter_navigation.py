from pathlib import Path
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.reader import ReaderCore


def test_chapter_navigation_basic(tmp_path: Path):
    """Test next/prev chapter navigation."""
    p = tmp_path / "multi_chapter.txt"
    content = """第一章 开始
这是第一章的内容。

第二章 发展
这是第二章的内容。

第三章 结局
这是第三章的内容。
"""
    p.write_text(content, encoding="utf-8")

    r = ReaderCore()
    r.load_txt(p)

    # Should have 3 chapters
    assert r.get_chapter_count() == 3
    assert r.get_current_chapter_index() == 0

    # Navigate forward
    assert r.next_chapter() is True
    assert r.get_current_chapter_index() == 1

    assert r.next_chapter() is True
    assert r.get_current_chapter_index() == 2

    # At last chapter, next should return False
    assert r.next_chapter() is False
    assert r.get_current_chapter_index() == 2

    # Navigate backward
    assert r.prev_chapter() is True
    assert r.get_current_chapter_index() == 1

    assert r.prev_chapter() is True
    assert r.get_current_chapter_index() == 0

    # At first chapter, prev should return False
    assert r.prev_chapter() is False
    assert r.get_current_chapter_index() == 0


def test_chapter_navigation_single_chapter(tmp_path: Path):
    """Test navigation with single chapter file."""
    p = tmp_path / "single.txt"
    content = "Just some text without chapter markers."
    p.write_text(content, encoding="utf-8")

    r = ReaderCore()
    r.load_txt(p)

    # Should have at least 1 chapter (fallback chunking)
    assert r.get_chapter_count() >= 1
    assert r.get_current_chapter_index() == 0

    # Navigation should return False (can't move)
    if r.get_chapter_count() == 1:
        assert r.next_chapter() is False
        assert r.prev_chapter() is False


def test_chapter_navigation_empty():
    """Test navigation with no file loaded."""
    r = ReaderCore()

    assert r.get_chapter_count() == 0
    assert r.get_current_chapter_index() == 0
    assert r.next_chapter() is False
    assert r.prev_chapter() is False


def test_set_chapter_index(tmp_path: Path):
    """Test set_chapter_index for restoring reading position."""
    p = tmp_path / "chapters.txt"
    content = """第一章 开始
内容一

第二章 发展
内容二

第三章 结局
内容三
"""
    p.write_text(content, encoding="utf-8")

    r = ReaderCore()
    r.load_txt(p)

    assert r.get_chapter_count() == 3

    # Set to valid index
    assert r.set_chapter_index(2) is True
    assert r.get_current_chapter_index() == 2

    assert r.set_chapter_index(0) is True
    assert r.get_current_chapter_index() == 0

    # Set to invalid index (out of range)
    assert r.set_chapter_index(10) is False
    assert r.get_current_chapter_index() == 0  # unchanged

    assert r.set_chapter_index(-1) is False
    assert r.get_current_chapter_index() == 0  # unchanged


def test_set_chapter_index_empty():
    """Test set_chapter_index with no file loaded."""
    r = ReaderCore()

    assert r.set_chapter_index(0) is False
    assert r.set_chapter_index(1) is False


def test_chapter_list_dialog():
    """Test ChapterListDialog functionality."""
    from PySide6.QtWidgets import QApplication
    from src.gui import ChapterListDialog

    app = QApplication.instance() or QApplication([])

    chapters = ["Chapter 1", "Chapter 2", "Chapter 3"]
    dialog = ChapterListDialog(chapters, 1)

    # Check if list is populated correctly
    assert dialog.list_widget.count() == 3
    assert dialog.list_widget.item(0).text() == "Chapter 1"

    # Check if current index is selected
    assert dialog.list_widget.currentRow() == 1

    # Test changing selection
    dialog.list_widget.setCurrentRow(2)
    assert dialog.get_selected_index() == 2
