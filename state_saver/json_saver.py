from .base import BaseStateSaver
from pathlib import Path
from typing import Dict
import json
from config.config_manager import get_config


def safe_serializer(obj):
    # 1. Try to convert Pydantic objects to dictionaries natively
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    elif hasattr(obj, 'dict'):
        return obj.dict()
    # 2. Fall back to your old trick for anything else (like datetime objects)
    return str(obj)

class JSONSaver(BaseStateSaver):
    
    def __init__(self, base_dir: Path | str | None=None):
        if base_dir is None:
            config_dir=None
            for target in get_config()["storage_targets"]:
                if target["type"]=="json":
                    config_dir=Path(target["output_dir"])
                    break
            if config_dir is None:
                raise ValueError("No 'json' type found in config storage_targets.")
            final_dir=config_dir
        else:
            final_dir=base_dir
        super().__init__(final_dir)
        
    def save(self, filename: str, data: dict):  
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                data, 
                f, 
                indent=4, 
                ensure_ascii=False, 
                default=safe_serializer
            )
    
    def load(self, filename: str) -> Dict | list:
        file_path = self.base_dir / f"{filename}.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)