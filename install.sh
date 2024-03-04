#!/usr/bin/env bash

# Package name
package_name="lst"

# Default installation path changed to ~/.local/share/$package_name
default_install_path="$HOME/.local/share/$package_name"

# Parse command-line arguments for custom install path, silent mode, or clone option
for arg in "$@"
do
    case $arg in
        --silent)
        silent="true"
        shift # Remove --silent from processing
        ;;
        --path=*)
        custom_install_path="${arg#*=}"
        shift # Remove --path=value from processing
        ;;
        --backup)
        backup="true"
        shift # Remove --backup from processing
        ;;
        --clone)
        clone_repo="true"
        shift # Remove --clone from processing
        ;;
    esac
done

install_path="${custom_install_path:-$default_install_path}"

# Function to echo only if not in silent mode
echo_if_not_silent() {
    if [ -z "$silent" ]; then
        echo "$@"
    fi
}

# Check for dependencies (example)
check_dependencies() {
    missing_deps=0
    command -v python3 >/dev/null 2>&1 || { echo_if_not_silent "python3 is not installed. Please install it and try again."; let missing_deps++; }
    if [ $missing_deps -ne 0 ]; then
        exit 1
    fi
}

# Clone the repository if needed
clone_repository() {
    if [ "$clone_repo" == "true" ]; then
        echo_if_not_silent "Cloning the repository..."
        git clone https://github.com/felipechierice/$package_name "$install_path"
        cd "$install_path" || exit
        echo_if_not_silent "Repository cloned to $install_path."
    fi
}

# Create virtual environment and install requirements
create_virtualenv_and_install_requirements() {
    local venv_path="$install_path/venv"
    echo_if_not_silent "Creating virtual environment in $venv_path."
    
    # Try using virtualenv first
    if command -v virtualenv >/dev/null 2>&1; then
        virtualenv "$venv_path"
    # Fallback to python -m venv
    elif command -v python3 >/dev/null 2>&1; then
        python3 -m venv "$venv_path"
    else
        echo_if_not_silent "Neither virtualenv nor python3 venv module is available. Please install one of them and try again."
        exit 1
    fi

    source "$venv_path/bin/activate"
    if [ -f "$(dirname "$0")/requirements.txt" ]; then
        pip install -r "$(dirname "$0")/requirements.txt"
        echo_if_not_silent "Requirements installed successfully."
    else
        echo_if_not_silent "No requirements.txt found. Skipping dependency installation."
    fi
    deactivate
}

# Backup existing installation
backup_if_needed() {
    if [ "$backup" == "true" ] && [ -d "$install_path" ]; then
        local timestamp=$(date +%Y%m%d-%H%M%S)
        local backup_path="${install_path}_backup_$timestamp"
        mv "$install_path" "$backup_path"
        echo_if_not_silent "Existing installation backed up to '$backup_path'"
    fi
}

# Modified installation steps
perform_installation() {
    if [ "$clone_repo" != "true" ]; then
        echo_if_not_silent "Attempting to install $package_name at '$install_path'."
        mkdir -p "$install_path"
        # Copy the current directory content to the new installation path
        cp -r "$(dirname "$0")/"* "$install_path"
    fi
    # Create a symbolic link to ~/.local/bin/$package_name
    ln -s "$install_path/$package_name" "$HOME/.local/bin/$package_name"
    echo_if_not_silent "Installation completed."
}

# Update PATH
update_path_in_shell() {
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
        echo_if_not_silent "Unsupported shell for automatic PATH update. Please manually add $install_path to your PATH."
        return
        ;;
    esac

    if ! grep -q "$install_path" "$shell_config_file" ; then
        echo "export PATH=\"$install_path:\$PATH\"" >> "$shell_config_file"
        echo_if_not_silent "Added $install_path to PATH in $shell_config_file."
    else
        echo_if_not_silent "$install_path is already in your PATH."
    fi
}

# Check if already installed and prompt for reinstallation
check_existing_installation() {
    if [ -d "$install_path" ] && [ "$clone_repo" != "true" ]; then
        if [ -z "$silent" ]; then
            read -p "$package_name is already installed. Do you want to proceed with reinstallation? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "Installation cancelled."
                exit 0
            fi
        fi
        backup_if_needed
    fi
}

main() {
    check_dependencies
    clone_repository
    check_existing_installation
    create_virtualenv_and_install_requirements
    perform_installation
    # Detect shell and ask user for input
    echo "You are using the $SHELL shell."
    read -p "Do you want to automatically add $HOME/.local/bin to your PATH? (y/n) " -n 1 -r
    echo # move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        update_path_in_shell
    else
        echo "Please add $HOME/.local/bin to your PATH manually."
    fi
    echo_if_not_silent "Installation completed successfully."
    echo_if_not_silent "Please restart your shell to start using $package_name."
}

main "$@"
