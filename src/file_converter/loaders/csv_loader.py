from pathlib import Path

import pandas as pd

from .base import BaseLoader


class CSVLoader(BaseLoader):
    """Loader for CSV format files."""

    def load(self, path: Path) -> pd.DataFrame:
        """Load CSV file from path.

        Args:
            path: Path to CSV file.

        Returns:
            Loaded DataFrame.

        Raises:
            pandas.errors.ParserError: If CSV is malformed.
        """
        return pd.read_csv(path)
