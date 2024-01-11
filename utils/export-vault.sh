#!/bin/bash

export_vault() {
    if [[ ! -d "$save_folder" ]];then
        echo "ERROR: Could not find the folder in which to save the files."
        exit 1
    fi

    if [[ ! $password1 ]]; then
        echo
        echo "Exporting personal vault to an unencrypted file..."
        bw export --format json --output "$save_folder"
    else
        echo 
        echo "Exporting personal vault to a password-encrypted file..."
        bw export --format encrypted_json --password "$password1" --output "$save_folder"
    fi
}