# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Diagram Renderer is a Python library for rendering text-based diagrams (Mermaid, PlantUML, Graphviz) into interactive HTML with zoom/pan controls. It includes multiple frontends: CLI, web dashboard, REST API, and MCP server.

## Development Commands

### Setup
```bash
# Install with all development dependencies
uv sync --extra dev

# Install specific extras
uv sync --extra cli        # CLI only
uv sync --extra dashboard  # Streamlit dashboard
uv sync --extra webapp     # FastAPI web app
uv sync --extra mcp        # MCP server
```

### Testing & Quality
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_diagram_renderer.py

# Run with coverage
uv run pytest --cov=diagram_renderer

# Run visual regression tests (requires baseline images)
python tests/visual/visual_test_runner.py

# Generate/update visual baselines
python tests/visual/baseline_generator.py

# Run only visual tests via pytest
pytest -m visual

# Code formatting (auto-fixes)
uv run ruff format .

# Linting
uv run ruff check .

# Type checking (currently has many annotation issues)
uv run mypy diagram_renderer

# Pre-commit hooks (install once)
uv run pip install pre-commit
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

### Release & Publishing
```bash
# Update version to current timestamp
uv run python scripts/update_version.py

# Build package for distribution
uv build

# Publish to PyPI (requires PYPI_API_TOKEN)
uv publish
```

### Running Applications
```bash
# CLI tool
uv run python examples/cli.py [options]

# Streamlit dashboard (requires dashboard extra)
uv run --extra dashboard streamlit run examples/dashboard.py

# FastAPI webapp (requires webapp extra)
uv run --extra webapp python examples/webapp.py

# MCP server (requires mcp extra)
uv run --extra mcp python examples/mcp_server.py
```

## Architecture

### Core Library Structure
- `diagram_renderer/__init__.py`: Main DiagramRenderer class that orchestrates rendering
- `diagram_renderer/renderers/base.py`: Abstract base class defining renderer interface
- `diagram_renderer/renderers/`: Individual renderer implementations (mermaid.py, plantuml.py, graphviz.py)
- `diagram_renderer/renderers/static/js/`: Bundled JavaScript libraries (self-contained, no CDN dependencies)
- `diagram_renderer/renderers/templates/`: Jinja2 templates for HTML generation

### Key Design Patterns
1. **Factory Pattern**: DiagramRenderer.render() automatically selects the appropriate renderer based on diagram type
2. **Template Method**: Each renderer inherits from BaseRenderer and implements `render_diagram()`
3. **Self-Contained Output**: All JavaScript dependencies are bundled locally to avoid external dependencies

### Adding New Diagram Types
1. Create new renderer in `diagram_renderer/renderers/` inheriting from `BaseRenderer`
2. Implement `render_diagram()` method
3. Update type detection in `DiagramRenderer._detect_diagram_type()`
4. Add tests in `tests/test_renderer.py`

## Important Notes

- **Python 3.10+** required
- Uses `uv` package manager (faster alternative to pip)
- All JavaScript libraries are pre-bundled in `static/js/` - do not use CDN versions
- HTML output includes both diagram and interactive controls in a single file
- Markdown support: Can extract and render diagrams from markdown code blocks

## Automated Release System

The project uses timestamp-based versioning (year.month.day.HHMM) and automated releases:

- **Automatic Releases**: GitHub Actions automatically detects conventional commits and creates releases
- **Trigger Commits**: `feat:`, `fix:`, `perf:`, `refactor:` commits trigger releases
- **Manual Release**: Use `workflow_dispatch` with `force_release: true` to manually trigger a release
- **Version Format**: `2025.8.3.1430` (Year.Month.Day.HourMinute in UTC)
- **Skip Release**: Add `[skip release]` or `[skip ci]` to commit messages to prevent releases
