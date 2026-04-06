# AGENTS.md for JSONBrotliMinifyer

## Dev environment tips
- Set up a virtual environment: `python -m venv .venv` and activate it with `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows).
- Install dependencies: `pip install -r requirements.txt` and `pip install -e .` for development.
- Use pre-commit hooks: Run `pre-commit install` to set up automatic linting and formatting on commits.
- Check Python version compatibility (supports 3.9+).

## Testing instructions
- Find the CI plan in the .github/workflows folder.
- Run `pytest` to run all tests.
- To focus on one test, use `pytest -k "<test name>"`.
- Fix any test or type errors until the whole suite is green.
- Run linting: `ruff check --fix` for linting and `ruff format` for formatting.
- Run type checking: `mypy .`
- After moving files or changing imports, run `ruff check` and `mypy` to ensure rules still pass.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions
- Title format: [feature/fix] <Title>
- Always run `pytest`, `ruff check --fix`, `ruff format`, and `mypy` before committing.