from __future__ import annotations
from typing import TypedDict, cast, NotRequired
from pathlib import Path
import tomllib


class Config(TypedDict):
    output_dir: str
    email: NotRequired[str]


def load(path: Path|str) -> Config:
    with open(Path(path), 'rb') as f:
        return cast(Config, tomllib.load(f))
