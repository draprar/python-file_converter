import pandas as pd
from pathlib import Path
from .base import BaseLoader


class PickleLoader(BaseLoader):
    def load(self, path: Path) -> pd.DataFrame:
        return pd.read_pickle(path)
