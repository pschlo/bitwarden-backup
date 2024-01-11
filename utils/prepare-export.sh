

prepare_export() {
    #Prompt the user for an encryption password
    echo -n "Enter a password to encrypt your vault export (or press ENTER for an unencrypted export): "
    read -s password1
    echo

    #Check if the user has decided to enter a password or save unencrypted
    if [[ ! $password1 ]]; then 
        echo -e -n "\033[0;33m" # set text = yellow
        echo "WARNING! Your vault contents will be saved to an unencrypted file."     
        echo -e -n "\033[0m" # set text = default color

        until [[ $CONTINUE =~ (y|n) ]]; do
            read -rp "Continue? [y/n]: " -e CONTINUE
        done

        if [[ $CONTINUE != "y" ]]; then
            echo "Exiting script."
            exit 1
        fi
    else
        echo -n "Enter the same password for verification: "
        read -s password2
        echo
        
        if [[ $password1 != $password2 ]]; then
            echo "ERROR: The passwords do not match."
            exit 1
        else
            echo "Passwords match. Be sure to save your password in a safe place!"
            echo
        fi
    fi
}