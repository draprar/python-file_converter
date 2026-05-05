# Contributing

Thanks for taking the time to contribute!

## Quick start

1. Fork the repo and create a feature branch.
2. Install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

3. Run checks before opening a PR:

```powershell
pytest --cov=src/file_converter --cov-fail-under=75
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/
python -m bandit -r src/
```

4. Auto-fix formatting issues:

```powershell
ruff format src/ tests/
```

## PR guidelines

- Keep changes focused and well-scoped.
- Add or update tests for behavior changes.
- Update documentation if you change user-facing behavior.
- Ensure CI is green before requesting review.

## Development

See [README.md](README.md) for project overview.

