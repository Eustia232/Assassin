from typing import Optional, List
from pydantic import BaseModel, Field


class Chapter(BaseModel):
    title: str = Field(..., description="章节标题或段落索引")
    text: str = Field(..., description="章节正文")


class BookMeta(BaseModel):
    title: str
    author: Optional[str] = None
    path: str


class StyleSettings(BaseModel):
    font_family: str = "Noto Sans"
    font_size: int = 18
    text_color: str = "#111111"
    bg_color: str = "#FFFFFF"
    auto_hide_enabled: bool = True
    auto_hide_delay_ms: int = 600
    hotkey: str = "Ctrl+Shift+H"
    chapter_rule_file: str = "默认.txt"
