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
