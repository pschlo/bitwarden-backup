#!/bin/bash

export_attachments() {
    if [[ $(get_items_with_attachments) != "" ]]; then
        echo
        echo "Saving attachments..."

        bash <(bw list items | jq -r '.[] 
        | select(.attachments != null) 
        | "bw get attachment \"\(.attachments[].fileName)\" --itemid \(.id) --output \"'$EXPORT_PATH'\(.name)/\""' )
    else
        echo
        echo "No attachments exist, so nothing to export."
    fi
}