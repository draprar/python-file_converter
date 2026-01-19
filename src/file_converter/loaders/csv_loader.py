import pandas as pd
from pathlib import Path
from .base import BaseLoader


class CSVLoader(BaseLoader):
    def load(self, path: Path) -> pd.DataFrame:
        return pd.read_csv(path)
