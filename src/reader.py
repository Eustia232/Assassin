from pathlib import Path
from typing import List
from .parser import read_text, split_into_chapters
from .models import Chapter


class ReaderCore:
    def __init__(self):
        self.chapters: List[Chapter] = []
        self.current_index: int = 0

    def load_txt(self, file_path: Path) -> None:
        text = read_text(file_path)
        self.chapters = split_into_chapters(text)
        self.current_index = 0

    def get_current_chapter_html(self) -> str:
        if not self.chapters:
            return ""
        chap = self.chapters[self.current_index]
        # Simple HTML escape and wrap
        body = chap.text.replace("\n", "<br/>")
        return f"<h2>{chap.title}</h2>\n<div>{body}</div>"
