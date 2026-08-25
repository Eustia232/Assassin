# Product Change Log

## 2026-08-25

### fix: Remove content-dependent minimum window width on Windows
- Set explicit `setMinimumSize(200, 100)` on MainWindow to override Qt's content-derived minimum
- Set QTextBrowser size policy to `Ignored` horizontally so book content no longer constrains window width
- Added `setMinimumWidth(0)` on QTextBrowser to fully remove widget-level minimum width hint
- Window can now be resized freely regardless of loaded book content

## 2026-07-20

### feat: Package Linux release as AppImage inside tar.gz
- Replaced raw PyInstaller binary with self-contained AppImage via linuxdeploy
- AppImage bundles Qt libraries for cross-distro portability, no system deps needed
- Added default blue icon for the AppImage .desktop entry
- Linux artifact is now a tar.gz containing the AppImage (mirrors Windows zip layout)

### fix: Replace linuxdeploy-plugin-qt with manual Qt plugin copy
- Removed qt6-base-dev and linuxdeploy-plugin-qt (qmake approach didn't find PySide6 Qt modules)
- linuxdeploy now auto-deploys shared libraries via ELF dependency scanning
- Manually copy Qt platform plugins from PySide6 package into AppDir

### fix: Use uv run for PySide6 import in AppImage build
- python3 couldn't find PySide6 (installed in uv venv), switched to uv run python3

### fix: Add libxcb-cursor0 dependency for xcb platform plugin
- Qt 6.5+ requires libxcb-cursor0 to load xcb platform plugin
- linuxdeploy now detects and bundles it automatically

## 2026-04-29

### feat: Support regex capture group for chapter titles
- Updated `src/parser.py` to use capture group 1 (`m.group(1)`) as the chapter title if present, falling back to full match. This allows stripping unwanted prefixes/suffixes from the displayed chapter list.
- Added `assets/regex/三国志.txt` with a regex rule to extract chapter names across multiple lines.
- Updated `README.md` to document the new regex capture group feature and `Ctrl+U` shortcut.

### feat: Add external regex rules with Ctrl+U selector
- Load chapter split rules from assets/regex text files and allow switching via Ctrl+U
- Reset reading position to the first chapter when a rule changes, with safe fallbacks on invalid rules
- Package Windows release with assets folder alongside the exe

### feat: Allow window opacity down to 0.1%
- Replaced integer slider with a decimal control and lowered minimum opacity

### feat: Show welcome text when no file is selected
- Added a default welcome message loaded from assets for empty reader state

### feat: Package Windows release as zip
- Publish a zip containing Assassin.exe for Windows releases

### fix: Add checkout step for release job
- Ensure release job runs inside a git repo for gh release commands

### feat: Add tag-based release workflow
- Added GitHub Actions workflow to build Windows/Linux packages on tag push
- Publishes a GitHub Release with both binaries attached

### docs: Add tag-based release packaging design
- Documented GitHub Actions workflow for Windows/Linux packaging on tag push

## 2026-04-02

### feat: Display scroll percentage in title bar
- Added real-time scroll percentage display in the title bar for current chapter
- Format: `Reader - filename.txt [1/10] 30%`
- Percentage updates dynamically as user scrolls through the chapter
- Shows `100%` when content fits without scrolling, `0%` at top, `100%` at bottom
