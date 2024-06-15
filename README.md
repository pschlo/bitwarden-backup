# bitwarden-backup
Small script to back up Bitwarden vault, including attachments



### Getting Started

1. Download Bitwarden CLI [here](https://bitwarden.com/download/)
2. Check if `pip` is available. If not, follow [these](https://pip.pypa.io/en/stable/installation/) steps.
3. Choose a release [here](https://github.com/pschlo/bw-backup/releases). Under the chosen release, look for an asset `bw_backup-x.x.x.tar.gz`. Copy the link to this asset.
4. Install bw-backup with `pip install [link to asset]`
5. Run the backup script with `python -m bw_backup`

### Optional: Encrypting the Backup

* encrypt:
  * `tar -cf [backup-name].tar [backup-name]`
  * `gpg --no-symkey-cache -co [backup-name].tar.gpg [backup-name].tar`
* decrypt:
  * `gpg --no-symkey-cache -do [backup-name].tar [backup-name].tar.gpg`
  * `tar -xf [backup-name].tar`
* clear GPG password cache: `gpg-connect-agent reloadagent /bye`

### Hints for backups with Tails OS

* Use standalone pip to avoid having to install it
* use `7z x` to extract the Bitwarden CLI
* Use `torify` to run both `pip install` and `python3 -m bw_backup`
