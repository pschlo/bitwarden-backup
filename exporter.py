from pathlib import Path
from pywarden import BitwardenControl, CliConfig, ApiConfig, Item, Attachment, UnlockedControl
import shutil


class Exporter:
  out_dir: Path
  email: str|None
  bw_control: BitwardenControl

  def __init__(self, out_dir: Path, email: str|None = None) -> None:
    self.out_dir = out_dir
    self.email = email
    self.bw_control = BitwardenControl(CliConfig(), ApiConfig())

  def run(self) -> None:
    self.create_out_dir()
    try:
      with self.bw_control.login_unlock_interactive(self.email) as ctl:
        self.save_json(ctl)
        items = self.get_items_with_attach(ctl)
        for item in items:
          self.save_attachments(item, ctl)
    except:
      print("Export failed, deleting output")
      shutil.rmtree(self.out_dir)
      raise

  def create_out_dir(self) -> None:
    if self.out_dir.exists():
      raise RuntimeError(f"Output folder already exists")
    self.out_dir.mkdir()

  def save_json(self, ctl: UnlockedControl) -> None:
    print("Creating JSON export")
    export = ctl.get_export()
    with (self.out_dir / 'export.json').open('w') as f:
      f.write(export)

  def get_items_with_attach(self, ctl: UnlockedControl) -> list[Item]:
    print("Fetching items")
    items = ctl.get_items()

    items_with_attach = list(filter(lambda x: x['attachments'], items))
    print(f"Found {len(items_with_attach)} items with attachments")
    return items_with_attach

  def save_attachments(self, item: Item, ctl: UnlockedControl):
    name = item['name']
    short_id = item['id'].split('-')[0]
    folder = self.out_dir / f"{name} ({short_id})"
    print(f"Getting attachments of item {name} ({short_id})")
    folder.mkdir()

    for attach in item['attachments']:
      self.save_attachment(folder, item, attach, ctl)

  def save_attachment(self, folder: Path, item: Item, attach: Attachment, ctl: UnlockedControl):
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
