import requests
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import subprocess
import stat
import tempfile
import tarfile
import sys


BW_CLI_VERSION = "2024.4.1"
BW_BACKUP_VERSION = "1.0.8"


def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir).resolve()

        print(f'Setting up bundle in {tmpdir}')
        setup_bundle(tmpdir)

        packfile = Path(f'bw_backup-{BW_BACKUP_VERSION}-bundle.tar.gz').resolve()
        print(f'Packing bundle to {packfile}')
        pack_bundle(tmpdir, packfile)


def make_executable(path: Path) -> None:
    new_mode = path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    path.chmod(new_mode)


def setup_bundle(out_dir: Path) -> None:
    print(f"Downloading Bitwarden CLI")
    r = requests.get(f'https://github.com/bitwarden/clients/releases/download/cli-v{BW_CLI_VERSION}/bw-linux-{BW_CLI_VERSION}.zip')
    r.raise_for_status()
    ZipFile(BytesIO(r.content)).extractall(out_dir)
    make_executable(out_dir / 'bw')

    print(f"Downloading bw-backup")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--target', str(out_dir), \
        f'https://github.com/pschlo/bw-backup/releases/download/v{BW_BACKUP_VERSION}/bw_backup-{BW_BACKUP_VERSION}.tar.gz'])

    print(f"Generating run.py")
    runfile = out_dir / "run.py"
    lines = [
        rf'#!/usr/bin/env python3',
        rf'import os; import sys; import subprocess; from pathlib import Path',
        rf'orig_path = Path.cwd()',
        rf'os.chdir(Path(__file__).parent.resolve())',
        rf'subprocess.run([sys.executable, "-m", "bw_backup", orig_path])',
    ]
    with open(runfile, 'w') as f:
        f.write("\n".join(lines))
    make_executable(runfile)


def pack_bundle(in_dir: Path, out_file: Path) -> None:
    with tarfile.open(out_file, "w:gz") as tar:
        outfile_stem = str(out_file.name).removesuffix(''.join(out_file.suffixes))
        tar.add(in_dir, arcname=outfile_stem)


if __name__ == '__main__':
    main()
