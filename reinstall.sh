#!/usr/bin/env bash

here=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Define paths to your install and uninstall scripts
INSTALL_SCRIPT_PATH="$here/install.sh"
UNINSTALL_SCRIPT_PATH="$here/uninstall.sh"

# Parse command-line arguments
for arg in "$@"
do
    case $arg in
        --silent)
        silent="true"
        ;;
        --path=*)
        install_path="${arg#*=}"
        ;;
        --backup)
        backup="true"
        ;;
    esac
done

# Reinstall function
reinstall_package() {
    # Construct uninstall command
    uninstall_command="$UNINSTALL_SCRIPT_PATH"
    if [ "$silent" == "true" ]; then
        uninstall_command+=" --silent"
    fi
    if [ ! -z "$install_path" ]; then
        uninstall_command+=" --path=$install_path"
    fi
    if [ "$backup" == "true" ]; then
        uninstall_command+=" --backup"
    fi

    # Run uninstall script
    echo "Running uninstallation script..."
    bash "$uninstall_command"

    # Check if uninstallation was successful
    if [ $? -ne 0 ]; then
        echo "Uninstallation failed. Aborting reinstallation."
        exit 1
    fi

    # Construct install command
    install_command="$INSTALL_SCRIPT_PATH"
    if [ "$silent" == "true" ]; then
        install_command+=" --silent"
    fi
    if [ ! -z "$install_path" ]; then
        install_command+=" --path=$install_path"
    fi
    if [ "$backup" == "true" ]; then
        install_command+=" --backup"
    fi

    # Run install script
    echo "Running installation script..."
    bash "$install_command"

    # Check if installation was successful
    if [ $? -eq 0 ]; then
        echo "Reinstallation completed successfully."
    else
        echo "Installation failed."
        exit 1
    fi
}

# Start the reinstallation process
reinstall_package "$@"
