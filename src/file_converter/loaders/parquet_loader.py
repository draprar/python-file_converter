from pathlib import Path

import pandas as pd

from .base import BaseLoader


class ParquetLoader(BaseLoader):
    """Loader for Apache Parquet format files."""

    def load(self, path: Path) -> pd.DataFrame:
        """Load Parquet file from path.

        Args:
            path: Path to Parquet file.

        Returns:
            Loaded DataFrame.

        Raises:
            pyarrow.ArrowException: If Parquet file is corrupt.
            FileNotFoundError: If file does not exist.
        """
        return pd.read_parquet(path)
