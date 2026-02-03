from pathlib import Path
from src.parser import split_into_chapters


def test_split_simple():
    text = "第1章 开始\n这里是正文。\n第2章 继续\n更多内容。"
    chaps = split_into_chapters(text)
    assert len(chaps) >= 2
    assert "第1章" in chaps[0].title
