from pathlib import Path

from src.progress import ProgressStore


def test_progress_save_and_load(tmp_path: Path):
    p = tmp_path / "book.txt"
    p.write_text("第1章 测试\n内容", encoding="utf-8")
    ps = ProgressStore(path=tmp_path / "progress.json")
    ps.save_progress(p, chapter_index=1, char_offset=42)
    ps.add_bookmark(p, offset=10, note="start")

    ps2 = ProgressStore(path=tmp_path / "progress.json")
    data = ps2.get_progress(p)
    assert data.get("chapter_index") == 1
    assert data.get("char_offset") == 42
    assert any(b.get("note") == "start" for b in data.get("bookmarks", []))
