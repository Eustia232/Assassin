# Tag-based Release Packaging Design

## Overview
Add a GitHub Actions workflow that builds Windows and Linux binaries on tag push
and publishes a GitHub Release with both artifacts attached. Packaging uses
PyInstaller and produces GUI-only Windows builds (no console window).

## Goals
- Build Windows and Linux binaries automatically when a tag is pushed.
- Publish a GitHub Release for the tag with both binaries attached.
- Keep packaging reproducible with existing PyInstaller spec file.

## Non-goals
- Add macOS packaging.
- Change runtime behavior beyond console window visibility.
- Add CI test execution in this first iteration.

## Architecture
The workflow uses three jobs:

1. build-windows (windows-latest)
   - Install Python 3.12 and uv
   - uv sync
   - Run PyInstaller using main.spec
   - Upload the built binary as an artifact

2. build-linux (ubuntu-latest)
   - Install Python 3.12 and uv
   - Install Qt runtime dependencies via apt
   - uv sync
   - Run PyInstaller using main.spec
   - Upload the built binary as an artifact

3. release (ubuntu-latest)
   - Download the two artifacts
   - Create GitHub Release for the tag
   - Attach both binaries to the release

## Data Flow
Tag push triggers the workflow. Each build job creates a platform-specific
binary with a tag-based name. Artifacts are persisted and then attached to a
GitHub Release for that tag.

## Error Handling
If either build job fails, the release job does not run. Action logs provide
the error details for diagnosis.

## Testing Strategy
No tests are executed in the workflow at this stage. Tests can be added later
as an optional pre-packaging step.

## Notes
- main.spec is updated to set console=False for GUI-only Windows builds.
- Output binary names include the tag for traceability.
