# Tabular Convert

Universal CLI tool for converting tabular data into a unified Pandas DataFrame and exporting it to CSV or Parquet.

## Features

- **Input formats**: CSV, Excel (.xlsx, .xls), JSON, Pickle, Parquet
- **Output formats**: CSV, Parquet (default)
- **Unified loading pipeline** via pandas
- **Data preview** with `--preview`
- **Clean empty columns** with `--drop-empty`
- **Project-based directory structure**: `data/input/` and `data/output/`

### ⚠️ Security Note: Pickle Format

Pickle files can execute arbitrary code on deserialization. **Only load pickle files from trusted sources.**

To enable pickle loading:
```
UNSAFE_PICKLE=1 convert data.pkl
```

---

## Installation

```
pip install .
```

Editable mode (recommended for development):

```
pip install -e .
```

---

## Usage

Basic conversion (default export to Parquet):

```
convert events.csv
```

Convert and export to CSV:

```
convert events.csv result.csv
```

Preview dataset structure:

```
convert events.csv --preview
```

Drop fully empty columns:

```
convert events.csv --drop-empty
```

List supported formats:

```
convert --list-formats
```

---

## Project Structure

```
project/
├── src/file_converter/
├── tests/
├── data/input/
├── data/output/
└── pyproject.toml
```

---

## Development

Run tests:

```
pytest
```

Tests are run automatically on GitHub Actions for every push and pull request to ensure code quality.

---

## License

MIT License.

## Author

[Walery](https://github.com/draprar)