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
PYWARDEN = "1.1.4"

OUT_DIR = Path("bundle")
SCRIPT = "run.py"


def download_github(project: str, release: str, asset: str) -> bytes:
    r = requests.get(rf'https://github.com/{project}/releases/download/{release}/{asset}')
    r.raise_for_status()
    return r.content

def unzip(content: bytes, dest: Path) -> None:
    f = ZipFile(BytesIO(content))
    f.extractall(dest)

def untar(content: bytes, dest: Path, *, path: Path = Path()) -> None:
    f = TarFile(fileobj=GzipFile(fileobj=BytesIO(content)))
    members = [m for m in f.getmembers() if Path(m.name).is_relative_to(path)]
    for m in members:
        m.name = str(Path(m.name).relative_to(path.parent))
    f.extractall(dest, members=members)

def make_executable(path: Path) -> None:
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


OUT_DIR.mkdir()


print(f"Downloading Bitwarden CLI")
cli_asset = download_github('bitwarden/clients', f'cli-v{BW_CLI}', f'bw-linux-{BW_CLI}.zip')
unzip(cli_asset, OUT_DIR)
make_executable(OUT_DIR / 'bw')


print(f"Downloading pywarden")
pywarden_asset = download_github('pschlo/pywarden', f'v{PYWARDEN}', f'pywarden-{PYWARDEN}.tar.gz')
untar(pywarden_asset, OUT_DIR, path=Path(f'pywarden-{PYWARDEN}', 'src', 'pywarden'))


print(f"Downloading bw-backup")
bw_backup_asset = download_github('pschlo/bw-backup', f'v{BW_BACKUP}', f'bw_backup-{BW_BACKUP}.tar.gz')
untar(bw_backup_asset, OUT_DIR, path=Path(f'bw_backup-{BW_BACKUP}', 'src', 'bw_backup'))


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
