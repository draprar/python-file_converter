from pathlib import Path
from typing import Union
import pandas as pd


def export_csv(df: pd.DataFrame, path: Union[str, Path]) -> None:
    """
    Export DataFrame to CSV format.
    
    Args:
        df: DataFrame to export.
        path: Output file path (str or Path object).
    """
    df.to_csv(path, index=False)


