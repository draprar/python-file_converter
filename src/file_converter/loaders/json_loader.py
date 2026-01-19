import json
from pathlib import Path
import pandas as pd

from .base import BaseLoader


class JSONLoader(BaseLoader):
    def load(self, path: Path) -> pd.DataFrame:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        df = pd.json_normalize(data)

        # --- automatyczne parsowanie datetime (najczęstszy case) ---
        datetime_candidates = [
            col for col in df.columns
            if "date" in col.lower() or "time" in col.lower()
        ]

        for col in datetime_candidates:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        return df
