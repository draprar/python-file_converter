import os
import pandas as pd
from pathlib import Path
from .base import BaseLoader


class PickleLoader(BaseLoader):
    """
    Load Pickle format data into a DataFrame.
    
    SECURITY WARNING: Pickle files can execute arbitrary code on deserialization.
    Only load pickle files from trusted sources.
    
    Enable via environment variable: UNSAFE_PICKLE=1
    """
    
    def load(self, path: Path) -> pd.DataFrame:
        if os.getenv("UNSAFE_PICKLE", "0").lower() not in ("1", "true"):
            raise RuntimeError(
                "Pickle loading is disabled by default (security risk).\n"
                "Only load pickle files from TRUSTED sources.\n"
                "To enable, set environment variable: UNSAFE_PICKLE=1"
            )
        return pd.read_pickle(path)

