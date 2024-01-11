#!/bin/bash

# Bitwarden CLI Vault Export Script

SCRIPT_DIR="$(dirname "$(realpath "$BASH_SOURCE")")"

source "$SCRIPT_DIR/env.sh"
for file in "$SCRIPT_DIR/utils/"*.sh; do
    source "$file"
done

unlock_vault
prepare_export
export_vault
export_organization
export_attachments

echo
echo "Exports completed."

check_trash