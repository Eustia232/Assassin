from pathlib import Path

from src.library import LibraryStore


def test_library_add_and_list(tmp_path: Path):
    p = tmp_path / "book.txt"
    p.write_text("第1章 测试\n内容", encoding="utf-8")

    lib = LibraryStore(path=tmp_path / "library.json")
    meta = lib.add_book(p)
    assert meta["title"]
    books = lib.list_books()
    assert any(b["path"] == str(p.resolve()) for b in books)
