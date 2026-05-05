from pathlib import Path
from typing import Union

import pandas as pd


def export_parquet(df: pd.DataFrame, path: Union[str, Path]) -> None:
    """
    Export DataFrame to Apache Parquet format.

    Args:
        df: DataFrame to export.
        path: Output file path (str or Path object).

    Raises:
        pyarrow.ArrowException: If write operation fails.
        PermissionError: If unable to write to path.
    """
    df.to_parquet(path, index=False)
