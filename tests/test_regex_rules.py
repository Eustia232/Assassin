import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.regex_rules import (
    DEFAULT_CHAPTER_REGEX,
    list_rule_files,
    load_rule_pattern,
)


def test_list_rule_files_sorted(tmp_path: pathlib.Path) -> None:
    regex_dir = tmp_path / "regex"
    regex_dir.mkdir()
    (regex_dir / "b.txt").write_text("^B$", encoding="utf-8")
    (regex_dir / "a.txt").write_text("^A$", encoding="utf-8")
    (regex_dir / "note.md").write_text("ignore", encoding="utf-8")

    files = list_rule_files(regex_dir)

    assert [p.name for p in files] == ["a.txt", "b.txt"]


def test_load_rule_valid(tmp_path: pathlib.Path) -> None:
    regex_dir = tmp_path / "regex"
    regex_dir.mkdir()
    (regex_dir / "rule.txt").write_text(r"^第.*章$", encoding="utf-8")

    pattern, error = load_rule_pattern(regex_dir, "rule.txt")

    assert pattern == r"^第.*章$"
    assert error is None


def test_load_rule_empty_fallback(tmp_path: pathlib.Path) -> None:
    regex_dir = tmp_path / "regex"
    regex_dir.mkdir()
    (regex_dir / "empty.txt").write_text("\n", encoding="utf-8")

    pattern, error = load_rule_pattern(regex_dir, "empty.txt")

    assert pattern == DEFAULT_CHAPTER_REGEX
    assert error is not None


def test_load_rule_invalid_fallback(tmp_path: pathlib.Path) -> None:
    regex_dir = tmp_path / "regex"
    regex_dir.mkdir()
    (regex_dir / "bad.txt").write_text("(", encoding="utf-8")

    pattern, error = load_rule_pattern(regex_dir, "bad.txt")

    assert pattern == DEFAULT_CHAPTER_REGEX
    assert error is not None
