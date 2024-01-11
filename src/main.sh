
main() {
    unlock_vault
    prepare_export
    export_vault
    export_organization
    export_attachments

    echo
    echo "Exports completed."

    check_trash
}