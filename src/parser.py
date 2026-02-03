from typing import List
import re
from pathlib import Path

from .models import Chapter


CHAPTER_RE = re.compile(r"^(第.*?章|CHAPTER\s+\w+)", re.I | re.M)


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
    """Split text into chapters using CHAPTER_RE. More robust than split() approach.

    Finds chapter headings and slices text between them. If no headings found,
    falls back to chunking by size.
    """
    matches = list(CHAPTER_RE.finditer(text))
    if not matches:
        # fallback: chunk by size (~10k chars)
        return [
            Chapter(title=f"Part {i + 1}", text=text[i : i + 10000])
            for i in range(0, len(text), 10000)
        ]

    chapters: List[Chapter] = []
    # preface before first chapter
    first = matches[0]
    if first.start() > 0:
        pre = text[: first.start()].strip()
        if pre:
            chapters.append(Chapter(title="Intro", text=pre))

    for idx, m in enumerate(matches):
        title = (m.group(1) or m.group(0)).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        chapters.append(
            Chapter(title=title or f"Chapter {len(chapters) + 1}", text=body)
        )

    return chapters
