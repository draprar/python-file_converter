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
    loader = LOADERS.get(path.suffix.lower())
    if not loader:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    return loader.load(path)
