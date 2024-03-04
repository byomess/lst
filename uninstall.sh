#!/usr/bin/env bash

# Package name
package_name="lst"

# Default installation path. Ensure this matches the installation script
default_install_path="$HOME/.local/share/$package_name"

# Parse command-line arguments for custom install path
for arg in "$@"; do
    case $arg in
        --path=*)
        custom_install_path="${arg#*=}"
        shift # Remove --path=value from processing
        ;;
    esac
done

install_path="${custom_install_path:-$default_install_path}"

# Function to echo messages
echo_message() {
    echo "$@"
}

# Remove the installed package directory
remove_package() {
    if [ -d "$install_path" ]; then
        rm -rf "$install_path"
        echo_message "Removed installed package at $install_path."
    else
        echo_message "Package directory $install_path does not exist."
    fi
}

# Remove the symbolic link from ~/.local/bin
remove_symlink() {
    local symlink_path="$HOME/.local/bin/$package_name"
    if [ -L "$symlink_path" ]; then
        rm "$symlink_path"
        echo_message "Removed symbolic link from $symlink_path."
    else
        echo_message "Symbolic link $symlink_path does not exist."
    fi
}

# Optionally remove the added path from the user's shell configuration file
remove_path_from_shell() {
    local shell_config_file
    case "$SHELL" in
    */bash)
        shell_config_file="$HOME/.bashrc"
        ;;
    */zsh)
        shell_config_file="$HOME/.zshrc"
        ;;
    */fish)
        shell_config_file="$HOME/.config/fish/config.fish"
        ;;
    *)
        echo_message "Automatic PATH removal is not supported for your shell. If you manually added $install_path to your PATH, please remove it."
        return
        ;;
    esac

    # Check and remove the path only if it was added
    if grep -q "$install_path" "$shell_config_file" ; then
        # Use sed to remove the line containing the path
        sed -i "/$install_path/d" "$shell_config_file"
        echo_message "Removed $install_path from PATH in $shell_config_file."
    else
        echo_message "$install_path was not found in your PATH in $shell_config_file."
    fi
}

main() {
    echo_message "Starting uninstallation of $package_name."
    remove_package
    remove_symlink
    read -p "Do you want to remove $install_path from your PATH in your shell configuration file? (y/n) " -n 1 -r
    echo # move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        remove_path_from_shell
    else
        echo_message "Skipping PATH removal. If you added $install_path to your PATH manually, please remove it."
    fi
    echo_message "Uninstallation completed. Please restart your shell."
}

main "$@"
