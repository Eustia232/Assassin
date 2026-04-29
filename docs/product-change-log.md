# Product Change Log

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
