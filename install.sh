#!/bin/bash

# Package name
package_name="lst"

# Default installation path
default_install_dir_path="$HOME/.local/share"

# Default binary path
default_bin_dir_path="$HOME/.local/bin"

# Entry point for the script
entry_point="lst.py"

# Default Python version for running the package
TARGET_PYENV_PYTHON_VERSION="3.11"

# Parse command-line arguments for custom install path, silent mode, or clone option
for arg in "$@"; do
	case $arg in
	--silent)
		silent="true"
		shift # Remove --silent from processing
		;;
	--path=*)
		custom_install_dir_path="${arg#*=}"
		shift # Remove --path=value from processing
		;;
	--bin-path=*)
		custom_bin_dir_path="${arg#*=}"
		shift # Remove --bin-path=value from processing
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

install_dir_path="${custom_install_dir_path:-$default_install_dir_path}"
bin_dir_path="${custom_bin_dir_path:-$default_bin_dir_path}"
bin_link_path="$bin_dir_path/$package_name"

package_install_dir_path="$install_dir_path/$package_name"
package_entry_point_path="$package_install_dir_path/$entry_point"
package_bin_path="$package_install_dir_path/$package_name"
package_python_bin_path="$package_install_dir_path/venv/bin/python"

# Function to echo only if not in silent mode
echo_if_not_silent() {
	if [ -z "$silent" ]; then
		echo "$@"
	fi
}

generate_entry_point_script() {
	cat <<EOF >"$package_bin_path"
#!/bin/bash
"$package_python_bin_path" "$package_entry_point_path" "\$@"
EOF

	chmod +x "$package_bin_path"
}

# Modified installation steps
perform_installation() {
	if [ "$clone_repo" != "true" ]; then
		echo_if_not_silent "Installing $package_name at '$package_install_dir_path'."
		mkdir -p "$install_dir_path"
		cp -r . "$package_install_dir_path"
	fi
	generate_entry_point_script
	ln -s "$package_bin_path" "$bin_link_path"
}

# Update PATH
update_path_in_shell() {
	local PATH_includes_bin_dir_path=false

	# Check if the path is already in the PATH
	if echo "$PATH" | grep -q "$(cd $bin_dir_path && pwd)"; then
		PATH_includes_bin_dir_path=true
	fi

	if [ "$PATH_includes_bin_dir_path" = true ]; then
		echo_if_not_silent "$bin_dir_path is already in your PATH."
		return
	fi

	echo_if_not_silent "$bin_dir_path is not in your PATH."
	echo_if_not_silent "You are using the $SHELL shell."
	read -p "Do you want to automatically add $HOME/.local/bin to your PATH? (y/N) " -n 1 -r
	echo_if_not_silent

	if [[ ! $REPLY =~ ^[Yy]$ ]]; then
		echo_if_not_silent "Please add $HOME/.local/bin to your PATH manually."
	fi

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
		echo_if_not_silent "Unsupported shell for automatic PATH update. Please manually add $bin_dir_path to your PATH."
		return
		;;
	esac

	echo "export PATH=\"$bin_dir_path:\$PATH\"" >>"$shell_config_file"

	echo_if_not_silent "Added $bin_dir_path to PATH in $shell_config_file."
}

# Check if already installed and prompt for reinstallation
check_existing_installation() {
	if [ -d "$package_install_dir_path" ] && [ "$clone_repo" != "true" ]; then
		if [ -z "$silent" ]; then
			read -p "$package_name is already installed. Do you want to proceed with reinstallation? (y/n) " -n 1 -r
			echo
			if [[ ! $REPLY =~ ^[Yy]$ ]]; then
				echo_if_not_silent "Installation cancelled."
				exit 0
			fi
		fi
		backup_if_needed
	fi
}

main() {
	check_existing_installation
	perform_installation
	generate_entry_point_script
	update_path_in_shell
	echo_if_not_silent "Installation completed."
}

main "$@"
