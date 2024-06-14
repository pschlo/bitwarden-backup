from __future__ import annotations
from pathlib import Path
from pywarden import BaseBwControl, UnlockedBwControl, Item, Attachment, CliConfig
import shutil
import logging
from datetime import datetime


log = logging.getLogger(__name__)

INDENT = 2


def guess_clipath() -> Path:
    # try finding in PATH
    r = shutil.which('bw')
    if r is not None:
        return Path(r)

    # try finding in current working dir
    r = Path.cwd() / 'bw'
    if r.exists():
        return r

    raise ValueError(f"Could not determine Bitwarden CLI path. Please provide it with '--cli'.")


def create_export(outdir_parent: Path|None = None, email: str|None = None, clipath: Path|None = None):
    clipath = clipath.resolve() if clipath is not None else guess_clipath()
    cli_conf = CliConfig(clipath)
    
    with BaseBwControl(cli_conf).login_unlock_interactive(email) as ctl:
        email = ctl.status()['userEmail']
        time = datetime.now().strftime("%Y-%m-%d_%H-%M")
        outdir = (outdir_parent or Path()) / f'bw-backup_{email}_{time}'
        outdir = outdir.resolve()
        outdir.mkdir()
        try:
            log.info(f'Starting export to "{outdir}"')
            _export(ctl, outdir)
        except:
            log.error("Export failed, deleting output")
            shutil.rmtree(outdir)
            raise


def _export(ctl: UnlockedBwControl, out_dir: Path) -> None:
    def main() -> None:
        save_json(out_dir)
        items = get_items_with_attach()
        if items:
            attachments_dir = out_dir / 'attachments'
            attachments_dir.mkdir()
            for item in items:
                save_attachments(attachments_dir, item)

    def save_json(dir: Path) -> None:
        log.info("Creating JSON export")
        export = ctl.get_export()
        with (dir / 'export.json').open('w') as f:
            f.write(export)

    def get_items_with_attach() -> list[Item]:
        log.info("Fetching items")
        items = ctl.get_items()

        items_with_attach = list(filter(lambda x: x['attachments'], items))
        log.info(f"Found {len(items_with_attach)} items with attachments")
        return items_with_attach

    def save_attachments(dir: Path, item: Item):
        name = item['name']
        short_id = item['id'].split('-')[0]
        log.info(1*INDENT*" " + f"Getting attachments of item '{name} ({short_id})'")

        item_dir = dir / f"{name} ({short_id})"
        item_dir.mkdir()

        for attach in item['attachments']:
            save_attachment(item_dir, item, attach)

    def save_attachment(dir: Path, item: Item, attach: Attachment):
        base_name = Path(f"{attach['fileName']}")
        name = base_name
        i = 1
        while (dir / name).exists():
            i += 1
            name = f"{base_name.stem} ({i}){base_name.suffix}"

        log.info(2*INDENT*" " + f"Fetching attachment '{name}'")
        content = ctl.get_attachment(item['id'], attach['id'])
        with (dir / name).open('wb') as f:
            f.write(content)

    return main()
