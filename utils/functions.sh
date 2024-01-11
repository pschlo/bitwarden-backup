#!/bin/bash

cleanup() {
    echo ""
    echo "Exiting; locking vault..."
    bw lock
    unset BW_SESSION
}
trap cleanup EXIT

bw_status() {
    bw status | jq -r .status
}

trash_count() {
    bw list items --trash | jq -r '. | length'
}

get_items_with_attachments() {
    bw list items | jq -r '.[] | select(.attachments != null)'
}

get_password() {
    echo -n "Enter your Bitwarden password: "
    read -s bw_password
    echo ""
}

login() {
    get_password
    export BW_SESSION="$(bw login "$EMAIL" "$bw_password" --method "$MFA_METHOD" --raw)"
}

unlock() {
    get_password
    export BW_SESSION="$(bw unlock "$bw_password" --raw)"
}


