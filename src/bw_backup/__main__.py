from pathlib import Path
from typing import Protocol, cast
import argparse
import logging

from .setup_logging import setup_logging
from .export import create_export


setup_logging(include_packages={'pywarden'})
log = logging.getLogger(__name__)


class Args(Protocol):
    output_dir: Path
    email: str | None


def get_args() -> Args:
    parser = argparse.ArgumentParser('bw-backup')
    parser.add_argument('output_dir', type=Path)
    parser.add_argument('--email', type=str)
    return cast(Args, parser.parse_args())

args = get_args()
create_export(args.output_dir, args.email)
