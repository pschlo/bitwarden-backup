import requests
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import subprocess
import stat
from tarfile import TarFile
from gzip import GzipFile
import sys


BW_CLI = "2024.4.1"
BW_BACKUP = "1.0.5"
PYWARDEN = "1.1.4"

BW_DATA_DIR = Path("bw_backup_data")
SCRIPT = "run-bw-backup"


BW_DATA_DIR.mkdir()

# print(f"Downloading Bitwarden CLI")
# r = requests.get(rf'https://github.com/bitwarden/clients/releases/download/cli-v{BW_CLI}/bw-linux-{BW_CLI}.zip')
# r.raise_for_status()
# ZipFile(BytesIO(r.content)).extractall(BW_DATA_DIR)

print(f"Downloading pywarden")
r = requests.get(rf'https://github.com/pschlo/pywarden/releases/download/v{PYWARDEN}/pywarden-{PYWARDEN}.tar.gz')
r.raise_for_status()
f = TarFile(fileobj=GzipFile(fileobj=BytesIO(r.content)))

prefix = f'pywarden-{PYWARDEN}/src/pywarden'
members = [m for m in f.getmembers() if m.name.startswith(prefix)]
for m in members:
    m.name = m.name.removeprefix(prefix).removeprefix('/')
f.extractall(BW_DATA_DIR / 'pywarden', members=members)


# print(f"Downloading bw-backup")
# r = requests.get(rf'https://github.com/pschlo/bw-backup/releases/download/v{BW_BACKUP}/bw_backup-{BW_BACKUP}.tar.gz')
# r.raise_for_status()
# TarFile(fileobj=GzipFile(fileobj=BytesIO(r.content))).extractall(BW_DATA_DIR)


sys.executable