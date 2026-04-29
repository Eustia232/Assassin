"""Tests for ReadingState persistence."""

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from src.reading_state import ReadingState


class TestReadingState:
    """Tests for ReadingState class."""

    def test_init_creates_empty_state_when_no_file(self, tmp_path: Path) -> None:
        """ReadingState initializes with empty data when file doesn't exist."""
        state_file = tmp_path / "reading_state.json"
        state = ReadingState(path=state_file)

        result = state.get_state()
        assert result["last_file"] is None
        assert result["chapter_index"] == 0
        assert result["scroll_position"] == 0

    def test_save_state_creates_file(self, tmp_path: Path) -> None:
        """save_state creates JSON file with correct content."""
        state_file = tmp_path / "reading_state.json"
        test_txt = tmp_path / "test.txt"
        test_txt.write_text("content", encoding="utf-8")

        state = ReadingState(path=state_file)
        state.save_state(file_path=test_txt, chapter_index=5, scroll_position=1234)

        assert state_file.exists()
        with state_file.open("r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
        assert data["last_file"] == str(test_txt.resolve())
        assert data["chapter_index"] == 5
        assert data["scroll_position"] == 1234

    def test_get_state_returns_saved_values(self, tmp_path: Path) -> None:
        """get_state returns previously saved values."""
        state_file = tmp_path / "reading_state.json"
        test_txt = tmp_path / "book.txt"
        test_txt.write_text("content", encoding="utf-8")

        state = ReadingState(path=state_file)
        state.save_state(file_path=test_txt, chapter_index=3, scroll_position=500)

        result = state.get_state()
        assert result["last_file"] == str(test_txt.resolve())
        assert result["chapter_index"] == 3
        assert result["scroll_position"] == 500

    def test_get_last_file_returns_path_if_exists(self, tmp_path: Path) -> None:
        """get_last_file returns Path when file exists."""
        state_file = tmp_path / "reading_state.json"
        test_txt = tmp_path / "existing.txt"
        test_txt.write_text("content", encoding="utf-8")

        state = ReadingState(path=state_file)
        state.save_state(file_path=test_txt)

        result = state.get_last_file()
        assert result is not None
        assert result == test_txt.resolve()

    def test_get_last_file_returns_none_if_file_deleted(self, tmp_path: Path) -> None:
        """get_last_file returns None when saved file no longer exists."""
        state_file = tmp_path / "reading_state.json"
        test_txt = tmp_path / "deleted.txt"
        test_txt.write_text("content", encoding="utf-8")

        state = ReadingState(path=state_file)
        state.save_state(file_path=test_txt)
        test_txt.unlink()  # Delete the file

        # Reload state to simulate app restart
        state2 = ReadingState(path=state_file)
        result = state2.get_last_file()
        assert result is None

    def test_state_persists_across_instances(self, tmp_path: Path) -> None:
        """State is preserved when creating new ReadingState instance."""
        state_file = tmp_path / "reading_state.json"
        test_txt = tmp_path / "persist.txt"
        test_txt.write_text("content", encoding="utf-8")

        # First instance saves state
        state1 = ReadingState(path=state_file)
        state1.save_state(file_path=test_txt, chapter_index=10, scroll_position=9999)

        # Second instance should load saved state
        state2 = ReadingState(path=state_file)
        result = state2.get_state()
        assert result["last_file"] == str(test_txt.resolve())
        assert result["chapter_index"] == 10
        assert result["scroll_position"] == 9999

    def test_save_state_with_none_file_path(self, tmp_path: Path) -> None:
        """save_state handles None file_path correctly."""
        state_file = tmp_path / "reading_state.json"

        state = ReadingState(path=state_file)
        state.save_state(file_path=None, chapter_index=0, scroll_position=0)

        result = state.get_state()
        assert result["last_file"] is None

    def test_load_handles_corrupted_file(self, tmp_path: Path) -> None:
        """ReadingState handles corrupted JSON file gracefully."""
        state_file = tmp_path / "reading_state.json"
        state_file.write_text("{ invalid json }", encoding="utf-8")

        state = ReadingState(path=state_file)
        result = state.get_state()

        # Should return defaults
        assert result["last_file"] is None
        assert result["chapter_index"] == 0
        assert result["scroll_position"] == 0

    def test_load_handles_non_dict_json(self, tmp_path: Path) -> None:
        """ReadingState handles non-dict JSON content gracefully."""
        state_file = tmp_path / "reading_state.json"
        state_file.write_text("[1, 2, 3]", encoding="utf-8")  # Array instead of object

        state = ReadingState(path=state_file)
        result = state.get_state()

        # Should return defaults
        assert result["last_file"] is None
        assert result["chapter_index"] == 0

    def test_reset_position(self, tmp_path: Path) -> None:
        state_file = tmp_path / "reading_state.json"
        test_txt = tmp_path / "book.txt"
        test_txt.write_text("content", encoding="utf-8")

        state = ReadingState(path=state_file)
        state.save_state(file_path=test_txt, chapter_index=3, scroll_position=500)

        state.reset_position(test_txt)

        result = state.get_state()
        assert result["chapter_index"] == 0
        assert result["scroll_position"] == 0
