#!/bin/bash
set -e

BW_CLI=2024.4.1
BW_BACKUP=1.0.5
PYWARDEN=1.1.4

BW_DATA_DIR=bw_backup_data
SCRIPT=run-bw-backup


mkdir $BW_DATA_DIR

wget https://github.com/bitwarden/clients/releases/download/cli-v$BW_CLI/bw-linux-$BW_CLI.zip
unzip bw-linux-$BW_CLI.zip
mv bw $BW_DATA_DIR
rm bw-linux-$BW_CLI.zip

wget https://github.com/pschlo/pywarden/releases/download/v$PYWARDEN/pywarden-$PYWARDEN.tar.gz
tar -xzf pywarden-$PYWARDEN.tar.gz
mv pywarden-$PYWARDEN/src/pywarden $BW_DATA_DIR
rm pywarden-$PYWARDEN.tar.gz
rm -r pywarden-$PYWARDEN

wget https://github.com/pschlo/bw-backup/releases/download/v$BW_BACKUP/bw_backup-$BW_BACKUP.tar.gz
tar -xzf bw_backup-$BW_BACKUP.tar.gz
mv bw_backup-$BW_BACKUP/src/bw_backup $BW_DATA_DIR
rm bw_backup-$BW_BACKUP.tar.gz
rm -r bw_backup-$BW_BACKUP

echo '#!/bin/bash' > $SCRIPT
echo "cd $BW_DATA_DIR" >> $SCRIPT
echo 'python3 -m bw_backup "$@"' >> $SCRIPT
chmod +x $SCRIPT
