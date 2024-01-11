
unlock_vault() {
    status_before="$(bw_status)"
    case $status_before in
        locked)
            echo "Vault locked, but already authenticated"
            unlock
            ;;
        unlocked)
            echo "Vault unlocked and authenticated"
            ;;
        unauthenticated)
            echo "Vault locked and unauthenticated"
            login
            ;;
        *)
            echo "Invalid Bitwarden status"
            exit 1
            ;;
    esac

    status_after="$(bw_status)"

    if [[ $status_after == "unauthenticated" ]]; then 
        echo "ERROR: Failed to authenticate."
        exit 1
    fi

    if ! [[ $status_after == "unlocked" && $BW_SESSION ]]; then 
        echo "ERROR: Failed to unlock."
        exit 1
    fi

    echo "Vault unlocked"
}