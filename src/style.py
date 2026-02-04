import re
from typing import Union
from .models import StyleSettings


HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")


def validate_color(value: str) -> bool:
    return bool(HEX_COLOR_RE.match(value))


def validate_hotkey(hotkey: str) -> bool:
    # Very small validation: must contain + and alphanumeric keys
    if not hotkey or "+" not in hotkey:
        return False
    parts = [p.strip() for p in hotkey.split("+") if p.strip()]
    if len(parts) < 2:
        return False
    # each part should be alnum or Ctrl/Shift/Alt
    for p in parts:
        if not re.match(r"^[A-Za-z0-9]+$", p):
            return False
    return True


def build_css(style: Union[StyleSettings, dict]) -> str:
    if isinstance(style, dict):
        s = style
    else:
        # pydantic v2 uses model_dump
        try:
            s = style.model_dump()
        except Exception:
            s = style.dict()

    font = s.get("font_family", "Noto Sans")
    size = int(s.get("font_size", 18))
    text_color = s.get("text_color", "#111111")
    bg_color = s.get("bg_color", "#FFFFFF")
    # default line-height reduced for denser layout; can be overridden by settings
    line_height = s.get("line_height", 1.3) if s.get("line_height") is not None else 1.3

    # sanitize/validate
    if not validate_color(text_color):
        text_color = "#111111"
    if not validate_color(bg_color):
        bg_color = "#FFFFFF"
    if size < 6:
        size = 6
    if size > 200:
        size = 200

    css = (
        f"body {{ font-family: '{font}'; font-size: {size}px; line-height: {line_height}; "
        f"color: {text_color}; background-color: {bg_color}; padding: 12px; }}"
    )
    return css


def wrap_html_with_style(inner_html: str, style: Union[StyleSettings, dict]) -> str:
    css = build_css(style)
    return f"<html><head><style>{css}</style></head><body>{inner_html}</body></html>"
