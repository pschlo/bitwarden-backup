from __future__ import annotations
from pathlib import Path
from pywarden import BitwardenControl, CliConfig, ApiConfig, Item, Attachment, UnlockedControl
import shutil


def create_export(out_dir: Path, email: str|None = None):
  if out_dir.exists():
    raise RuntimeError(f"Output folder already exists")
  out_dir.mkdir()

  try:
    base_ctl = BitwardenControl(CliConfig(), ApiConfig())
    with base_ctl.login_unlock_interactive(email) as ctl:
      _export(ctl, out_dir)
  except:
    print("Export failed, deleting output")
    shutil.rmtree(out_dir)
    raise


def _export(ctl: UnlockedControl, out_dir: Path) -> None:
  def main() -> None:
    save_json()
    items = get_items_with_attach()
    for item in items:
      save_attachments(item)

  def save_json() -> None:
    print("Creating JSON export")
    export = ctl.get_export()
    with (out_dir / 'export.json').open('w') as f:
      f.write(export)

  def get_items_with_attach() -> list[Item]:
    print("Fetching items")
    items = ctl.get_items()

    items_with_attach = list(filter(lambda x: x['attachments'], items))
    print(f"Found {len(items_with_attach)} items with attachments")
    return items_with_attach

  def save_attachments(item: Item):
    name = item['name']
    short_id = item['id'].split('-')[0]
    folder = out_dir / f"{name} ({short_id})"
    print(f"Getting attachments of item '{name} ({short_id})'")
    folder.mkdir()

    for attach in item['attachments']:
      save_attachment(folder, item, attach)

  def save_attachment(folder: Path, item: Item, attach: Attachment):
    base_name = Path(f"{attach['fileName']}")
    name = base_name
    i = 1
    while (folder / name).exists():
      i += 1
      name = f"{base_name.stem} ({i}){base_name.suffix}"

    print(f"Fetching attachment '{name}'")
    content = ctl.get_attachment(item['id'], attach['id'])
    with (folder / name).open('wb') as f:
      f.write(content)

  return main()
