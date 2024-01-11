#!/bin/bash

export_organization() {
    if [[ $org_id ]]; then 
        if [[ ! $password1 ]]; then
            echo
            echo "Exporting organization vault to an unencrypted file..."
            bw export --organizationid "$org_id" --format json --output "$save_folder"
        else
            echo 
            echo "Exporting organization vault to a password-encrypted file..."
            bw export --organizationid "$org_id" --format encrypted_json --password "$password1" --output "$save_folder"
        fi
    else
        echo
        echo "No organizational vault exists, so nothing to export."
    fi
}