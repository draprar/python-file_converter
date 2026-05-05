from pathlib import Path

import pandas as pd

from .base import BaseLoader


class ExcelLoader(BaseLoader):
    """Loader for Excel format files (.xlsx, .xls)."""

    def load(self, path: Path) -> pd.DataFrame:
        """Load Excel file from path.

        Args:
            path: Path to Excel file (.xlsx or .xls).

        Returns:
            Loaded DataFrame from first sheet.

        Raises:
            pandas.errors.InvalidFile: If Excel file is corrupt.
            FileNotFoundError: If file does not exist.
        """
        return pd.read_excel(path)
