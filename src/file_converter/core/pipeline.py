from pathlib import Path
import pandas as pd

from file_converter.loaders.csv_loader import CSVLoader
from file_converter.loaders.excel_loader import ExcelLoader
from file_converter.loaders.json_loader import JSONLoader
from file_converter.loaders.pickle_loader import PickleLoader
from file_converter.loaders.parquet_loader import ParquetLoader


LOADERS = {
    ".csv": CSVLoader(),
    ".xlsx": ExcelLoader(),
    ".xls": ExcelLoader(),
    ".json": JSONLoader(),
    ".pkl": PickleLoader(),
    ".pickle": PickleLoader(),
    ".parquet": ParquetLoader(),
}


def load_file(path: str) -> pd.DataFrame:
    path = Path(path)

    if not path.exists():
        raise ValueError(f"Input file does not exist: {path}")

    suffix = path.suffix.lower()
    loader = LOADERS.get(suffix)

    if not loader:
        supported = ", ".join(sorted(LOADERS.keys()))
        raise ValueError(
            f"Unsupported input format: {suffix}\nSupported: {supported}"
        )

    return loader.load(path)