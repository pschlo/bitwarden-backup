# bitwarden-backup
Small script to back up Bitwarden vault, including attachments



### Getting Started

1. Download Bitwarden CLI [here](https://bitwarden.com/download/)
2. Check if `pip` is available. If not, follow [these](https://pip.pypa.io/en/stable/installation/) steps.
3. Choose a release [here](https://github.com/pschlo/bw-backup/releases). Under the chosen release, look for an asset `bw_backup-x.x.x.tar.gz`. Copy the link to this asset.
4. Install bw-backup with `pip install [link to asset]`
5. Run the backup script with `python -m bw_backup`

### Optional: Encrypting the Backup

* encrypt with `gpgtar -co [backup-name].tar.gpg [backup-name]`
* decrypt with `gpgtar -dC . [backup-name].tar.gpg `

### Hints for backups from a live OS

* for installing bw-backup, standalone pip might be the easiest option
