from abc import ABC, abstractmethod
from typing import Any, Dict
from pathlib import Path

class BaseStateSaver(ABC):
    def __init__(self, base_dir: Path | str):
        self.base_dir = Path(base_dir)
        # Ensure the output directory exists
        self.base_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def save(self, filename: str, data: Any) -> Path:
        """
        Saves the state or result to the storage medium.
        Must be implemented by concrete classes.
        """
        pass
    
    @abstractmethod
    def load(self, filename: str) -> Any:
        """Loads and returns the data from the storage medium."""
        pass