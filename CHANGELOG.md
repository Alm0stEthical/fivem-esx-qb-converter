# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-02-24

### Changed
- Rewrote entire codebase for clarity and correctness
- Replaced class-based UI components with simple functions
- Consolidated all patterns into flat module-level lists (no more factory function)
- Moved dependency specification to `pyproject.toml`
- Simplified converter to 3 clean functions with no dead parameters
- Proper `app.shutdown()` instead of `sys.exit(0)`

### Fixed
- ~30 duplicate entries in QB-Core-to-ESX pattern list
- `manual_replace()` running unconditionally regardless of conversion direction (removed; init patterns are now in the pattern lists themselves)
- XSS vulnerability in output console (file paths are now HTML-escaped)
- Broken `ui.get_time()` call replaced with `datetime.now()`
- Broken SQL patterns toggle (removed non-functional feature entirely)
- Double error handling in `process_file` / `process_folder`

### Removed
- Dead duplicate file `src/ui/app.py`
- Empty `src/utils/` package
- Unused dependencies: `pathlib`, `pydantic`, `typing-extensions`
- Unused `import re`
- `requirements.txt` (replaced by `pyproject.toml`)
- `__pycache__` files from git tracking
- Excessive docstrings and redundant comments

### Added
- `pyproject.toml` with semantic versioning (`2.0.0`)
- `__version__` in `src/__init__.py`
- Version display in UI header
- `.gitignore` (expanded)
- This changelog
- GitHub Actions CI workflow (lint only)
- GitHub Actions release workflow (tag-based)

## [1.0.0] - 2024

Initial release with ESX/QB-Core conversion via NiceGUI web interface.
