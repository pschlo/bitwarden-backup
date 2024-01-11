#!/bin/bash

# Bitwarden CLI Vault Export Script

SCRIPT_DIR="$(dirname "$(realpath "$BASH_SOURCE")")"

source "$SCRIPT_DIR/env.sh"
for file in "$SCRIPT_DIR/src/"*.sh; do
    source "$file"
done

main