from typing import List, Optional
import re
from pathlib import Path

from .models import Chapter
from .regex_rules import DEFAULT_CHAPTER_REGEX

try:
    from charset_normalizer import from_bytes
except ImportError:
    from_bytes = None


def detect_encoding(file_path: Path) -> str:
    """Detect file encoding using charset_normalizer, fallback to common encodings."""
    raw = file_path.read_bytes()

    # Try charset_normalizer first
    if from_bytes is not None:
        result = from_bytes(raw).best()
        if result is not None:
            return result.encoding

    # Fallback: try common encodings
    for enc in ["utf-8", "gbk", "gb2312", "gb18030", "cp1252"]:
        try:
            raw.decode(enc)
            return enc
        except Exception:
            continue

    return "utf-8"  # ultimate fallback


def read_text(file_path: Path, encoding: str = None) -> str:
    if encoding is None:
        encoding = detect_encoding(file_path)
    with file_path.open("r", encoding=encoding, errors="replace") as f:
        return f.read()


def split_into_chapters(text: str, chapter_pattern: Optional[str] = None) -> List[Chapter]:
    """Split text into chapters using a regex pattern. More robust than split() approach.

    Finds chapter headings and slices text between them. If no headings found,
    falls back to chunking by size.
    """
    pattern = chapter_pattern or DEFAULT_CHAPTER_REGEX
    chapter_re = re.compile(pattern, re.I | re.M)
    matches = list(chapter_re.finditer(text))
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
        title = (m.group(1) if m.groups() else m.group(0)).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        chapters.append(
            Chapter(title=title or f"Chapter {len(chapters) + 1}", text=body)
        )

    return chapters
