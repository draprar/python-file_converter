from pathlib import Path
from typing import Union
import pandas as pd


def export_parquet(df: pd.DataFrame, path: Union[str, Path]) -> None:
    """
    Export DataFrame to Parquet format.
    
    Args:
        df: DataFrame to export.
        path: Output file path (str or Path object).
    """
    df.to_parquet(path, index=False)


