from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class BaseLoader(ABC):
    """Abstract base class for all file format loaders."""

    @abstractmethod
    def load(self, path: Path) -> pd.DataFrame:
        """Load file into a pandas DataFrame.

        Args:
            path: Path to the file to load.

        Returns:
            Loaded DataFrame.

        Raises:
            Various: Format-specific errors (see concrete implementations).
        """
