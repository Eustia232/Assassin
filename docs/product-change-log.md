# Product Change Log

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

## 2026-04-29

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
