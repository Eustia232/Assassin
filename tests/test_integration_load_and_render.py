from pathlib import Path
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.reader import ReaderCore
from src.style import wrap_html_with_style


def test_load_and_render(tmp_path: Path):
    # create a simple txt
    p = tmp_path / "sample.txt"
    p.write_text("第1章 测试\n内容一\n第2章 二\n内容二", encoding="utf-8")

    reader = ReaderCore()
    reader.load_txt(p, chapter_pattern=r"^第\d+章")
    html = reader.get_current_chapter_html()
    # wrap with default style
    wrapped = wrap_html_with_style(html, {})
    assert "<h2>" in wrapped
    assert "内容一" in wrapped
