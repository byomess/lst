#!/usr/bin/env bash

# Package name
package_name="lst"

# Default installation path
default_install_path="$HOME/.local/share"

# Default binary path
default_bin_path="$HOME/.local/bin"

# Entry point for the script
entry_point="lst.py"

# Parse command-line arguments for custom install path or binary path
for arg in "$@"; do
	case $arg in
	--silent)
		silent="true"
		shift # Remove --silent from processing
		;;
	--path=*)
		custom_install_path="${arg#*=}"
		shift # Remove --path=value from processing
		;;
	--bin-path=*)
		custom_bin_path="${arg#*=}"
		shift # Remove --bin-path=value from processing
		;;
	esac
done

install_path="${custom_install_path:-$default_install_path}"
bin_path="${custom_bin_path:-$default_bin_path}"
package_install_dir_path="$install_path/$package_name"
entry_point_path="$package_install_dir_path/$entry_point"

# Function to echo only if not in silent mode
echo_if_not_silent() {
	if [ -z "$silent" ]; then
		echo "$@"
	fi
}

# Uninstall the package
perform_uninstallation() {
	if [ -L "$bin_path/$package_name" ]; then
		rm "$bin_path/$package_name"
		echo_if_not_silent "Removed symbolic link from $bin_path/$package_name"
	else
		echo_if_not_silent "No symbolic link found at $bin_path/$package_name"
	fi

	if [ -d "$package_install_dir_path" ]; then
		rm -rf "$package_install_dir_path"
		echo_if_not_silent "Removed package directory $package_install_dir_path"
	else
		echo_if_not_silent "Package directory not found at $package_install_dir_path"
	fi
}

main() {
	perform_uninstallation
	echo_if_not_silent "Uninstallation completed successfully."
}

main "$@"
