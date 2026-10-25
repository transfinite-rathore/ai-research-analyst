import yaml
from pathlib import Path


from functools import lru_cache

@lru_cache(maxsize=1)
def get_config() -> dict:
    """
    Loads the YAML configuration file. 
    lru_cache(maxsize=1) ensures file I/O happens only once.
    """
    # Resolves the path relative to this Python file's location
    current_dir = Path(__file__).parent
    config_path = current_dir / "config.yaml"
    
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
