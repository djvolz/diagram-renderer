# Repository Guidelines

## Project Structure & Module Organization
`diagram_renderer/` hosts the core library, the CLI entrypoint (`cli.py`), and renderer backends in `renderers/` (`mermaid.py`, `plantuml.py`, `graphviz.py`) alongside HTML templates and bundled JS. Examples for dashboards, the FastAPI web app, the MCP server, and CLI demos live under `examples/`. Feature-focused tests sit in `tests/`, guided by `pytest.ini` and `pyproject.toml`, while project automation scripts (such as `update_version.py`) are grouped in `scripts/`.

## Build, Test, and Development Commands
Install dependencies with `uv sync --extra all`, or target extras like `uv sync --extra dashboard`. Format and lint via `uv run ruff format .` and `uv run ruff check . --fix`. Static typing is enforced with `uv run mypy diagram_renderer`. Run unit tests using `uv run pytest -v`, switch markers with `-m 'not slow'`, and capture coverage through `uv run pytest --cov=diagram_renderer`. Generate distributable artifacts with `uv build`, and wire pre-commit hooks using `uv run pre-commit install` followed by `uv run pre-commit run -a`.

## Coding Style & Naming Conventions
Target Python 3.10+, four-space indentation, and Ruff's 100-character line limit. Prefer explicit imports ordered stdlib / third-party / local, avoid wildcards, and keep public APIs type-annotated—`pyproject.toml` enables `disallow_untyped_defs`. Follow naming conventions: `snake_case` for modules and functions, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants.

## Testing Guidelines
Write Pytest suites in `tests/test_*.py`, reusing fixtures from `tests/conftest.py` to keep coverage concise. Mark integration or slow scenarios with `@pytest.mark.integration` and `@pytest.mark.slow`, letting CI skip expensive paths by default. Validate renderer output with deterministic HTML or asset assertions from `diagram_renderer/renderers/static/`. Aim for meaningful coverage metrics (`uv run pytest --cov=diagram_renderer`) before submitting changes.

## Commit & Pull Request Guidelines
Use Conventional Commits such as `feat(renderer): add svg sanitizer` to clarify scope. Each PR should summarize changes, link any issues, and attach screenshots or sample HTML for UI-affecting work. Confirm lint, typing, and tests have been run (report commands in the PR description), keep diffs focused, and respond promptly to review feedback.

## Security & Configuration Tips
Ship assets from the repository—do not add CDN dependencies or remote script tags. Large binaries belong in `diagram_renderer/renderers/static/` and should be referenced relatively so offline demos remain functional. Avoid network calls in automated tests, and review dependency updates for licensing and supply-chain risk before merging.
