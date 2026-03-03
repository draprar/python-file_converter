# Tabular Convert

Universal CLI tool for converting tabular data into a unified Pandas DataFrame and exporting it to CSV or Parquet.

## Features

- Supports input formats:
  - CSV
  - Excel (.xlsx, .xls)
  - JSON
  - Pickle
  - Parquet
- Unified DataFrame loading pipeline
- Export to:
  - CSV
  - Parquet (default)
- Optional:
  - Dataset preview
  - Drop empty columns
- Project-based directory structure (`data/input`, `data/output`)

---

## Installation

```bash
pip install .
```

Editable mode (recommended for development):

```
pip install -e .
```

---

## 

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

CI runs automatically on push and pull requests.