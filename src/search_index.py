from pathlib import Path
import sqlite3
from typing import List, Tuple


def build_index(chapters: List[Tuple[int, str]], db_path: Path) -> None:
    """Build a simple FTS5 index for chapters.

    chapters: list of (chapter_index, text)
    db_path: path to sqlite file
    """
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS chapter_fts USING fts5(chapter_index, content)"
        )
        cur.executemany(
            "INSERT INTO chapter_fts (chapter_index, content) VALUES (?, ?)", chapters
        )
        conn.commit()
    finally:
        conn.close()


def search_index(
    query: str, db_path: Path, limit: int = 10
) -> List[Tuple[int, float, str]]:
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT chapter_index, rank, content FROM chapter_fts WHERE chapter_fts MATCH ? LIMIT ?",
            (query, limit),
        )
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()
