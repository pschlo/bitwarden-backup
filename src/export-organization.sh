#!/bin/bash

export_organization() {
    if [[ $ORG_ID ]]; then 
        if [[ ! $password1 ]]; then
            echo
            echo "Exporting organization vault to an unencrypted file..."
            bw export --organizationid "$ORG_ID" --format json --output "$EXPORT_PATH"
        else
            echo 
            echo "Exporting organization vault to a password-encrypted file..."
            bw export --organizationid "$ORG_ID" --format encrypted_json --password "$password1" --output "$EXPORT_PATH"
        fi
    else
        echo
        echo "No organizational vault exists, so nothing to export."
    fi
}