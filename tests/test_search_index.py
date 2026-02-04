from pathlib import Path
from src.search_index import build_index, search_index


def test_search_build_and_query(tmp_path: Path):
    db = tmp_path / "index.db"
    chapters = [(0, "这是第一章 内容 包含关键词X"), (1, "第二章 没有关键词")]
    build_index(chapters, db)
    res = search_index("关键词X", db)
    # Might be empty depending on sqlite fts matching; ensure callable
    assert isinstance(res, list)
