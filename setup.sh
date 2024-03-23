#!/usr/bin/env bash

# Package name
package_name="lst"

# Parse command-line arguments for silent mode or clone option
for arg in "$@"; do
	case $arg in
	--silent)
		silent="true"
		shift # Remove --silent from processing
		;;
	--clone)
		clone_repo="true"
		shift # Remove --clone from processing
		;;
	esac
done

# Function to echo only if not in silent mode
echo_if_not_silent() {
	if [ -z "$silent" ]; then
		echo "$@"
	fi
}

# Check for dependencies (example)
check_dependencies() {
	missing_deps=0
	command -v python3 >/dev/null 2>&1 || {
		echo_if_not_silent "python3 is not installed. Please install it and try again."
		let missing_deps++
	}
	if [ $missing_deps -ne 0 ]; then
		exit 1
	fi
}

# Clone the repository if needed
clone_repository() {
	if [ "$clone_repo" == "true" ]; then
		echo_if_not_silent "Cloning the repository..."
		git clone https://github.com/felipechierice/$package_name .
		echo_if_not_silent "Repository cloned to the current directory."
	fi
}

# Create virtual environment and install requirements
create_virtualenv_and_install_requirements() {
	local venv_path="./venv"
	echo_if_not_silent "Creating virtual environment in $venv_path."

	# Try using virtualenv first
	if command -v virtualenv >/dev/null 2>&1; then
		virtualenv "$venv_path"
	# Fallback to python -m venv
	elif command -v python3 >/dev/null 2>&1; then
		python -m venv "$venv_path"
	else
		echo_if_not_silent "Neither virtualenv nor python3 venv module is available. Please install one of them and try again."
		exit 1
	fi

	source "$venv_path/bin/activate"

	if [ -f "requirements.txt" ]; then
		pip install -r "requirements.txt"
		echo_if_not_silent "Requirements installed successfully."
	else
		echo_if_not_silent "No requirements.txt found. Skipping dependency installation."
	fi
	deactivate
}

main() {
	check_dependencies
	clone_repository
	create_virtualenv_and_install_requirements
	echo_if_not_silent "Package setup completed successfully."
}

main "$@"
