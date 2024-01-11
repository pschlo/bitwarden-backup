#!/bin/bash

export_vault() {
    if [[ ! -d "$EXPORT_PATH" ]]; then
        echo "ERROR: Could not find the folder in which to save the files."
        exit 1
    fi

    if [[ ! $password1 ]]; then
        echo
        echo "Exporting personal vault to an unencrypted file..."
        bw export --format json --output "$EXPORT_PATH"
    else
        echo 
        echo "Exporting personal vault to a password-encrypted file..."
        bw export --format encrypted_json --password "$password1" --output "$EXPORT_PATH"
    fi
}