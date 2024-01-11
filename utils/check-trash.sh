

check_trash() {
    # Report items in the Trash (cannot be exported)
    if (($(trash_count) > 0)); then
        echo -e -n "\033[0;33m" # set text = yellow
        echo "Note: You have $trash_count items in the trash that cannot be exported."
        echo -e -n "\033[0m" # set text = default color
    fi
}