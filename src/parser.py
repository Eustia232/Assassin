from typing import List
import re
from pathlib import Path

from .models import Chapter


CHAPTER_RE = re.compile(r"^(第[\s\S]{0,20}章|CHAPTER\s+\w+)", re.I | re.M)


def detect_encoding(file_path: Path) -> str:
    """Simple encoding detection fallback. Try utf-8 then cp1252."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            f.read(1024)
        return "utf-8"
    except Exception:
        return "cp1252"


def read_text(file_path: Path, encoding: str = None) -> str:
    if encoding is None:
        encoding = detect_encoding(file_path)
    with file_path.open("r", encoding=encoding, errors="replace") as f:
        return f.read()


def split_into_chapters(text: str) -> List[Chapter]:
    parts = CHAPTER_RE.split(text)
    if len(parts) <= 1:
        # fallback: chunk by size (~10k chars)
        return [
            Chapter(title=f"Part {i + 1}", text=text[i : i + 10000])
            for i in range(0, len(text), 10000)
        ]
    chapters: List[Chapter] = []
    pre = parts[0].strip()
    if pre:
        chapters.append(Chapter(title="Intro", text=pre))
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        chapters.append(
            Chapter(title=title or f"Chapter {len(chapters) + 1}", text=body)
        )
    return chapters
