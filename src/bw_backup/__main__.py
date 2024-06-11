from pathlib import Path

from .config import load as load_config
from .export import create_export


config = load_config("./config.toml")

create_export(Path(config["output_dir"]), config.get('email', None))
