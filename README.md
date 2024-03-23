<p align="center">
    <img width="200px" src="https://github.com/byomess/lst/blob/main/images/logo.png?raw=true" align="center" alt="LS Turbo Logo" />
    <h2 align="center">lst - ls turbo</h2>
    <p align="center">🔥 Your <code>ls</code> command on <strong>turbo</strong> 🚀</p>
</p>

<p align="center">
    <a href="https://github.com/felipechierice/lst/stargazers">
        <img src="https://img.shields.io/github/stars/felipechierice/lst?style=social" alt="GitHub stars">
    </a>
    <a href="https://github.com/felipechierice/lst/network/members">
        <img src="https://img.shields.io/github/forks/felipechierice/lst?style=social" alt="GitHub forks">
    </a>
    <a href="https://github.com/felipechierice/lst/issues">
        <img src="https://img.shields.io/github/issues/felipechierice/lst" alt="GitHub issues">
    </a>
    <a href="https://github.com/felipechierice/lst/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/felipechierice/lst" alt="GitHub license">
    </a>
    <a href="https://github.com/felipechierice/lst/graphs/contributors">
        <img src="https://img.shields.io/github/contributors/felipechierice/lst" alt="GitHub contributors">
    </a>
    <a href="https://github.com/felipechierice/lst/commits/main">
        <img src="https://img.shields.io/github/last-commit/felipechierice/lst" alt="GitHub last commit">
    </a>
</p>

<p align="center">
    <img src="https://github.com/byomess/lst/blob/main/images/ss-1.png?raw=true" align="center" alt="LS Turbo Screenshot" />
</p>

`lst` is an enhanced version of the traditional `ls` command found in Linux systems, designed to provide a more informative and visually appealing way to list files and directories. It leverages the power of the [Rich library](https://github.com/willmcgugan/rich) to display outputs in a colorful, structured, and easy-to-read format. Whether you're navigating through cluttered directories or you need detailed file information at a glance, `lst` offers a plethora of features to make directory listing more insightful and productive.

`lst` draws inspiration from [lsd](https://github.com/lsd-rs/lsd). Much like `lsd`, `lst` aims to enhance the user experience by incorporating advanced features such as rich formatting, icons and detailed file information, but with some extras.

## Key Features

- **Directory Size Calculations**: Can show the total size of directories with the `--show-folder-size | -x` option, a feature not available in the standard `ls` command.
- **Rich Visual Outputs**: Utilizes Rich's capabilities to display file and directory listings with beautiful syntax highlighting, making them easier to read and understand.
- **Nerd Font Icons**: Integrates beautifully designed icons from [Nerd Fonts](https://www.nerdfonts.com/) for file types, directories, and various file extensions, making the output not only informative but also visually engaging. Whether it's a music file, a script, or a directory, `lst` displays an intuitive icon next to each item, enhancing the user's ability to quickly identify file types at a glance.
- **Customizable Displays**: Offers several options to customize the output, such as showing hidden files, sorting by various attributes (name, size, creation date, modification date), and toggling visibility of file and directory details (permissions, owner, group, size).
- **Color-Coded File Types and Permissions**: Files and directories are color-coded based on type (e.g., directory, executable file) and permissions, offering a quick overview of their attributes.
- **Advanced Sorting Options**: In addition to the standard alphabetical sorting, `lst` allows sorting by size, creation date, and modification date, with an option to reverse the sorting order.

## Why Use lst?

While the traditional `ls` command is powerful, `lst` takes file listing to the next level with its rich visual outputs and detailed information display. It's particularly useful for:

- Developers and system administrators who frequently interact with the filesystem and need a quick, informative overview of directory contents.
- Users looking for a more user-friendly and informative alternative to `ls`.
- Those who need to quickly assess file and directory sizes, permissions, and modifications at a glance.

## Installation

You can install `lst` using curl, wget, or by manually cloning the repository and installing dependencies. 

### Using Curl

```bash
curl -sSL "https://raw.githubusercontent.com/felipechierice/lst/main/install.sh" | bash -s -- --clone
```

### Using Wget

```bash
wget -qO- "https://raw.githubusercontent.com/felipechierice/lst/main/install.sh" | bash -s -- --clone
```

### Manual Installation

If you prefer to install `lst` manually, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/felipechierice/lst
```

2. Navigate to the `lst` directory:

```bash
cd lst
```

3. Execute the installation script

```bash
./install.sh
```

Ensure you have Python 3.6 or later installed on your system to use `lst`.

## Usage

The `lst` command enhances your file and directory listing with a rich set of features. Below is a detailed guide on how to use `lst` to its full potential.

### Basic Usage

- **List current directory contents**: Simply type `lst` to list the files and directories in your current working directory.
  
  ```bash
  lst
  ```

- **List contents of a specific directory**: To list items in a specific directory, provide the path as an argument.
  
  ```bash
  lst /path/to/directory
  ```

### Display Options

- **Table format**: Use the `-t` or `--table` option to display the contents in a table format, making it easier to read.
  
  ```bash
  lst -t
  ```

- **Show table header**: To add a header to the table format, include the `-H` or `--show-header` option.
  
  ```bash
  lst -tH # Same as: ls -t -H
  ```

- **Include hidden files**: The `-a` or `--all` flag will include hidden files (those starting with a dot) in the listing.
  
  ```bash
  lst -ta
  ```

### Sorting and Filtering

- **Sort by attribute**: Use the `-s` or `--sort-by` option followed by your choice of `name`, `size`, `created`, or `modified` to sort the listing accordingly.
  
  ```bash
  lst -ts size
  ```

- **Reverse sorting**: The `-r` or `--reverse-sorting` flag reverses the sorting order of the listing.
  
  ```bash
  lst -trs size # Same as: lst -t -r -s size
  ```

### Detailed Information

- **Show creation and modification dates**: Display the creation date with `-c` or `--show-created` and the modification date with `-m` or `--show-modified`.
  
  ```bash
  lst -tcm
  ```

- **Show file sizes**: The `-b` or `--show-size` option shows the size of files and directories.
  
  ```bash
  lst -tb
  ```

- **Show total size of directories**: To see the total size of each directory listed, use `-x` or `--show-folder-size`.
  
  ```bash
  lst -tx
  ```

- **Show permissions, owner, and group**: Display permissions with `-p` or `--show-permissions`, owner with `-u` or `--show-owner`, and group with `-g` or `--show-group`.
  
  ```bash
  lst -tpug
  ```

### Advanced Usage

- **Comprehensive listing**: Combine multiple options to get a detailed overview, for example, a table with sizes, permissions, owner, group, and modification dates of all files, including hidden ones.
  
  ```bash
  lst -tHabpuagms size
  ```

- **Quiet mode**: The `-q` or `--quiet` option suppresses progress bars and other non-essential output, useful for scripting or when you need a clean output.
  
  ```bash
  lst -txbq
  ```

By mastering these options, you can tailor the `lst` output to precisely fit your needs, making file and directory management a visually enjoyable and efficient process.

### Useful Aliases

```bash
# List files in table format with headers, file size, permissions and creation date
alias ll='lst -Hpbc'
```

Put this on your `.bashrc` (or any other shell config file) and use `ll` to have a very handy alias.
You can still run it with additional flags like `ll -x` to include directory sizes in the listing.

Here are some more handy `lst` aliases you might want to use:
```bash
alias l='lst $@' # List directory entries in short format
alias ll='lst -Hpbc $@' # List directory entries in table format
alias lll='lst -Hpbcmug $@' # List directory entries in table format with more info
alias la='lst -a $@' # List directory entries (including hidden) in short format
alias lla='lst -Hpbac $@'  # List directory entries (including hidden) in table format
alias llla='lst -Hpbacmug $@'  # List directory entries (including hidden) in table forma with more infot
```

## Uninstalling

It is as simple as executing the following script:

```bash
~/.local/share/lst/uninstall.sh
```

If you have installed `lst` in a different directory, just make sure you change it in the command.

## Contributing

Contributions are welcome! If you have suggestions for improvements, feel free to fork the repository and submit a pull request.

## License

`lst` is open-source software licensed under the MIT license.
