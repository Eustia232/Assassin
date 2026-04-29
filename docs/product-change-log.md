# Product Change Log

## 2026-04-29

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
