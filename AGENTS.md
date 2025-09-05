# Repository Guidelines

## Project Structure & Module Organization
- `diagram_renderer/`: Core library, CLI (`cli.py`), renderers (`renderers/` with `mermaid.py`, `plantuml.py`, `graphviz.py`), templates and static JS assets.
- `examples/`: Dashboard (`dashboard.py`), FastAPI app (`webapp.py`), MCP server, CLI demos.
- `tests/`: Pytest suite organized by feature; `pytest.ini` and `pyproject.toml` define markers/options.
- `scripts/`: Utility scripts (e.g., `update_version.py`).

## Build, Test, and Development Commands
- Install deps: `uv sync --extra all` (or selective extras: `dashboard`, `webapp`, `mcp`).
- Lint (fix): `uv run ruff check . --fix` and Format: `uv run ruff format .`.
- Type check: `uv run mypy diagram_renderer`.
- Run tests: `uv run pytest -v` (markers: `-m 'not slow'`). Coverage: `uv run pytest --cov=diagram_renderer`.
- Pre-commit: `uv run pre-commit install` then `uv run pre-commit run -a`.
- Build package: `uv build`.

## Coding Style & Naming Conventions
- Python 3.10+; 4-space indentation; max line length 100 (Ruff config).
- Names: modules/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`.
- Imports: group stdlib/third-party/local; prefer explicit imports; avoid wildcard.
- Tools: Ruff for lint/format; MyPy with `disallow_untyped_defs=true` (add/propagate type hints).

## Testing Guidelines
- Framework: Pytest; tests live in `tests/`, files `test_*.py`.
- Use markers (`@pytest.mark.integration`, `@pytest.mark.slow`) and keep unit tests fast/deterministic.
- Add tests with clear Given/When/Then structure; prefer fixture reuse from `tests/conftest.py`.
- Validate HTML output with string/DOM assertions and sample assets under `renderers/static/`.

## Commit & Pull Request Guidelines
- Commits: follow Conventional Commits (`feat:`, `fix:`, `chore:`, `refactor:`, `style:`). Example: `fix(tests): update UI icon assertion`.
- PRs: concise title/description, link issues, list changes, include before/after screenshots or sample HTML for UI changes, and test plan (`pytest -v`, markers used).
- Passing CI, lint, type checks required; keep PRs focused and small.

## Security & Configuration Tips
- Assets are self-hosted; avoid adding CDN dependencies.
- Keep large static files under `diagram_renderer/renderers/static/` and reference relatively.
- Prefer offline-friendly examples; avoid network calls in tests.
