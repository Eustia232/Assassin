from pathlib import Path
from typing import List, Optional
from .parser import read_text, split_into_chapters
from .models import Chapter


class ReaderCore:
    def __init__(self):
        self.chapters: List[Chapter] = []
        self.current_index: int = 0

    def load_txt(self, file_path: Path, chapter_pattern: Optional[str] = None) -> None:
        text = read_text(file_path)
        self.chapters = split_into_chapters(text, chapter_pattern=chapter_pattern)
        self.current_index = 0

    def get_current_chapter_html(self) -> str:
        if not self.chapters:
            return ""
        chap = self.chapters[self.current_index]
        # Simple HTML escape and wrap
        body = chap.text.replace("\n", "<br/>")
        return f"<h2>{chap.title}</h2>\n<div>{body}</div>"

    def next_chapter(self) -> bool:
        """Move to next chapter. Returns True if moved, False if already at last."""
        if not self.chapters:
            return False
        if self.current_index < len(self.chapters) - 1:
            self.current_index += 1
            return True
        return False

    def prev_chapter(self) -> bool:
        """Move to previous chapter. Returns True if moved, False if already at first."""
        if not self.chapters:
            return False
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    def get_chapter_count(self) -> int:
        """Return total number of chapters."""
        return len(self.chapters)

    def get_current_chapter_index(self) -> int:
        """Return current chapter index (0-based)."""
        return self.current_index

    def set_chapter_index(self, index: int) -> bool:
        """Set current chapter index. Returns True if valid, False otherwise."""
        if not self.chapters:
            return False
        if 0 <= index < len(self.chapters):
            self.current_index = index
            return True
        return False
