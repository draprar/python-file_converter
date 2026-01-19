from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


class BaseLoader(ABC):
    @abstractmethod
    def load(self, path: Path) -> pd.DataFrame:
        pass
