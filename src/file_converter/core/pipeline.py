from pathlib import Path
from typing import Union

import pandas as pd
from tqdm import tqdm

from file_converter.loaders.csv_loader import CSVLoader
from file_converter.loaders.excel_loader import ExcelLoader
from file_converter.loaders.json_loader import JSONLoader
from file_converter.loaders.parquet_loader import ParquetLoader
from file_converter.loaders.pickle_loader import PickleLoader

# Default maximum file size: 1GB
DEFAULT_MAX_FILE_SIZE = 1_000_000_000  # 1 GB in bytes


LOADERS = {
    ".csv": CSVLoader(),
    ".xlsx": ExcelLoader(),
    ".xls": ExcelLoader(),
    ".json": JSONLoader(),
    ".pkl": PickleLoader(),
    ".pickle": PickleLoader(),
    ".parquet": ParquetLoader(),
}


def load_file(path: Union[str, Path], max_size: int = DEFAULT_MAX_FILE_SIZE) -> pd.DataFrame:
    """
    Load tabular data from a file into a pandas DataFrame.

    Args:
        path: File path (str or Path object).
        max_size: Maximum allowed file size in bytes (default: 1GB).

    Returns:
        Loaded DataFrame.

    Raises:
        ValueError: If file does not exist, format is unsupported, or file is too large.
    """
    path = Path(path)

    if not path.exists():
        raise ValueError(f"Input file does not exist: {path}")

    # Check file size
    file_size = path.stat().st_size
    if file_size > max_size:
        file_size_mb = file_size / 1_000_000
        max_size_mb = max_size / 1_000_000
        raise ValueError(
            f"File too large: {file_size_mb:.1f}MB (maximum allowed: {max_size_mb:.1f}MB)\n"
            "Use a smaller file or contact developer to increase limit."
        )

    suffix = path.suffix.lower()
    loader = LOADERS.get(suffix)

    if not loader:
        supported = ", ".join(sorted(LOADERS.keys()))
        raise ValueError(f"Unsupported input format: {suffix}\nSupported: {supported}")

    # Show progress bar for large files (>100MB)
    file_size_mb = file_size / 1_000_000
    if file_size_mb > 100:
        print(f"Loading large file ({file_size_mb:.1f}MB)...")
        with tqdm(total=file_size_mb, desc="Loading", unit="MB", unit_scale=False) as pbar:
            # This is a placeholder for future enhancement
            pbar.update(file_size_mb)

    return loader.load(path)
