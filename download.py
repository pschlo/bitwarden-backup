import requests
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import subprocess
import stat
from tarfile import TarFile
from gzip import GzipFile
import sys
import os


BW_CLI = "2024.4.1"
BW_BACKUP = "1.0.5"
OUT_DIR = Path("bundle")
SCRIPT = "run.py"


def make_executable(path: Path) -> None:
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


OUT_DIR.mkdir()


print(f"Downloading Bitwarden CLI")
r = requests.get(f'https://github.com/bitwarden/clients/releases/download/cli-v{BW_CLI}/bw-linux-{BW_CLI}.zip')
r.raise_for_status()
ZipFile(BytesIO(r.content)).extractall(OUT_DIR)
make_executable(OUT_DIR / 'bw')


print(f"Downloading bw-backup")
subprocess.run([sys.executable, '-m', 'pip', 'install', '--target', str(OUT_DIR), \
    f'https://github.com/pschlo/bw-backup/releases/download/v{BW_BACKUP}/bw_backup-{BW_BACKUP}.tar.gz'])


lines = [
    rf'#!/usr/bin/env python3',
    rf'import os; import sys; import subprocess; from pathlib import Path',
    rf'path = Path(__file__).parent.resolve()',
    rf'os.chdir(path)',
    rf'subprocess.run([sys.executable, "-m", "bw_backup"])',
]
with open(Path(OUT_DIR / SCRIPT), 'w') as f:
    f.write("\n".join(lines))
make_executable(OUT_DIR / SCRIPT)
