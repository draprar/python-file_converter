import os
from pathlib import Path
from typing import cast

import pandas as pd

from .base import BaseLoader


class PickleLoader(BaseLoader):
    """
    SECURITY NOTE:
    Pickle is inherently unsafe. Only enable for trusted sources.
    """

    def load(self, path: Path) -> pd.DataFrame:
        if os.getenv("UNSAFE_PICKLE", "0").lower() not in ("1", "true"):
            raise RuntimeError(
                "Pickle loading disabled (unsafe by default). "
                "Enable via UNSAFE_PICKLE=1 only for trusted files."
            )

        # SECURITY: pickle enabled only via UNSAFE_PICKLE env flag (trusted input gate)
        obj = pd.read_pickle(path)  # nosec B301

        if not isinstance(obj, pd.DataFrame):
            raise TypeError(
                f"Expected pandas DataFrame, got {type(obj).__name__}"
            )

        return cast(pd.DataFrame, obj)
