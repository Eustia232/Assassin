import sys
import pathlib

# Ensure project root is on sys.path so `src` package is importable during tests
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.parser import split_into_chapters


def test_split_simple():
    text = "第1章 开始\n这里是正文。\n第2章 继续\n更多内容。"
    chaps = split_into_chapters(text)
    assert len(chaps) >= 2
    assert "第1章" in chaps[0].title


def test_split_with_custom_regex():
    text = "SECTION A\nAlpha\nSECTION B\nBeta"
    chaps = split_into_chapters(text, chapter_pattern=r"^SECTION\s+\w+")
    assert len(chaps) == 2
    assert chaps[0].title == "SECTION A"
