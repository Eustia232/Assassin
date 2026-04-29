from pathlib import Path
from typing import List, Optional, Tuple
import re

DEFAULT_CHAPTER_REGEX = r"^(第.*?章|CHAPTER\s+\w+)"


def list_rule_files(regex_dir: Path) -> List[Path]:
    if not regex_dir.exists():
        return []
    if not regex_dir.is_dir():
        return []
    files = [
        p
        for p in regex_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".txt"
    ]
    return sorted(files, key=lambda p: p.name.lower())


def _read_rule_file(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None


def load_rule_pattern(regex_dir: Path, rule_file: Optional[str]) -> Tuple[str, Optional[str]]:
    if not rule_file:
        return DEFAULT_CHAPTER_REGEX, "rule_file_missing"
    path = regex_dir / rule_file
    if not path.exists() or not path.is_file():
        return DEFAULT_CHAPTER_REGEX, "rule_file_not_found"
    text = _read_rule_file(path)
    if text is None:
        return DEFAULT_CHAPTER_REGEX, "rule_file_unreadable"
    pattern = text.strip()
    if not pattern:
        return DEFAULT_CHAPTER_REGEX, "rule_file_empty"
    try:
        re.compile(pattern)
    except re.error:
        return DEFAULT_CHAPTER_REGEX, "rule_invalid"
    return pattern, None
