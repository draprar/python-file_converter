import json
from pathlib import Path
import pandas as pd

from .base import BaseLoader


class JSONLoader(BaseLoader):
    """
    Load JSON data into a DataFrame with optional datetime parsing.
    
    Supports two datetime parsing modes:
    1. Auto-detect: Set environment variable PARSE_JSON_DATETIME=1
       Parses columns containing 'date' or 'time' in name as datetime (use with caution).
    2. Safe (default): No automatic datetime conversion.
    """
    
    def load(self, path: Path) -> pd.DataFrame:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        df = pd.json_normalize(data)

        # Optional: Parse datetime columns only if explicitly enabled
        # This prevents silent conversion of columns like "runtime", "timestamp_text"
        import os
        if os.getenv("PARSE_JSON_DATETIME", "0").lower() in ("1", "true"):
            datetime_candidates = [
                col for col in df.columns
                if "date" in col.lower() or "time" in col.lower()
            ]
            for col in datetime_candidates:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        return df

