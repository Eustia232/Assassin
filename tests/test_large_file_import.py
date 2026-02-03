from pathlib import Path
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.reader import ReaderCore


def test_large_file_import(tmp_path: Path):
    p = tmp_path / "large.txt"
    # create a ~50KB file
    content = "第1章 起\n" + ("内容行\n" * 2000)
    p.write_text(content, encoding="utf-8")

    r = ReaderCore()
    r.load_txt(p)
    assert len(r.chapters) >= 1
    assert "第1章" in r.chapters[0].title or "Part" in r.chapters[0].title
