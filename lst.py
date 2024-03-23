import stat
import os
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TaskID
from datetime import datetime, timedelta
import re
from pwd import getpwuid
from grp import getgrgid

extensions = {
    "mp3": "[yellow][/] ",
    "wav": "[yellow][/] ",
    "m4a": "[yellow][/] ",
    "ogg": "[yellow][/] ",
    "flac": "[yellow][/] ",
    "aac": "[yellow][/] ",
    "wma": "[yellow][/] ",
    "aiff": "[yellow][/] ",
    "alac": "[yellow][/] ",
    "ape": "[yellow][/] ",
    "opus": "[yellow][/] ",
    "pcm": "[yellow][/] ",
    "ac3": "[yellow][/] ",
    "amr": "[yellow][/] ",
    "mid": "[yellow][/] ",
    "mp4": "[red][/] ",
    "avi": "[red][/] ",
    "mkv": "[red][/] ",
    "mov": "[red][/] ",
    "wmv": "[red][/] ",
    "flv": "[red][/] ",
    "webm": "[red][/] ",
    "m4v": "[red][/] ",
    "mpeg": "[red][/] ",
    "3gp": "[red][/] ",
    "ts": "[red][/] ",
    "vob": "[red][/] ",
    "rm": "[red][/] ",
    "rmvb": "[red][/] ",
    "ogv": "[red][/] ",
    "styl": " ",
    "sass": " ",
    "scss": " ",
    "htm": "[red][/] ",
    "html": "[red][/] ",
    "slim": "[red][/] ",
    "ejs": "[red][/] ",
    "css": "[blue][/] ",
    "less": "[blue][/] ",
    "json": "[yellow][/] ",
    "js": "[yellow1][/] ",
    "mjs": "[yellow1][/] ",
    "jsx": "[cyan][/] ",
    "rb": "[red][/] ",
    "php": "[blue][/] ",
    "py": "[yellow][/] ",
    "pyc": "[yellow][/] ",
    "pyo": "[yellow][/] ",
    "pyd": "[yellow][/] ",
    "coffee": "[brown][/] ",
    "mustache": " ",
    "hbs": " ",
    "conf": "[white][/] ",
    "ini": "[white][/] ",
    "yml": "[white][/] ",
    "yaml": "[white][/] ",
    "toml": "[white][/] ",
    "bat": "[white][/] ",
    "jpg": "[magenta][/] ",
    "jpeg": "[magenta][/] ",
    "bmp": "[magenta][/] ",
    "png": "[magenta][/] ",
    "webp": "[magenta][/] ",
    "gif": "[magenta][/] ",
    "ico": "[magenta][/] ",
    "twig": " ",
    "cpp": "[white][/] ",
    "c++": "[white][/] ",
    "cxx": "[white][/] ",
    "cc": "[white][/] ",
    "cp": "[white][/] ",
    "c": "[white][/] ",
    "cs": " ",
    "h": "[white][/] ",
    "hh": "[white][/] ",
    "hpp": "[white][/] ",
    "hxx": "[white][/] ",
    "hs": " ",
    "lhs": " ",
    "lua": "[blue][/] ",
    "java": "[red][/] ",
    "sh": "[green][/] ",
    "fish": "[green][/] ",
    "bash": "[green][/] ",
    "zsh": "[green][/] ",
    "ksh": "[green][/] ",
    "csh": "[green][/] ",
    "awk": "[green][/] ",
    "ps1": "[green][/] ",
    "ml": "λ ",
    "mli": "λ ",
    "diff": " ",
    "db": "[white][/] ",
    "sql": "[white][/] ",
    "dump": "[white][/] ",
    "clj": " ",
    "cljc": " ",
    "cljs": " ",
    "edn": " ",
    "scala": " ",
    "go": " ",
    "dart": " ",
    "xul": "[orange][/] ",
    "sln": "[blue][/] ",
    "suo": "[blue][/] ",
    "pl": "[magenta][/] ",
    "pm": "[magenta][/] ",
    "t": "[magenta][/] ",
    "rss": " ",
    "f#": " ",
    "fsscript": " ",
    "fsx": " ",
    "fs": " ",
    "fsi": " ",
    "rs": " ",
    "rlib": " ",
    "d": " ",
    "erl": " ",
    "hrl": " ",
    "ex": "[magenta][/] ",
    "exs": "[magenta][/] ",
    "eex": "[magenta][/] ",
    "leex": "[magenta][/] ",
    "vim": "[green4][/] ",
    "ai": "[orange][/] ",
    "psd": "[blue][/] ",
    "psb": "[blue][/] ",
    "ts": "[dodger_blue1][/] ",
    "tsx": "[cyan][/] ",
    "jl": " ",
    "pp": " ",
    "vue": "﵂ ",
    "elm": " ",
    "swift": " ",
    "xcplayground": " ",
    "txt": "[bright_white][/] ",
    "log": " ",
    "md": "[red][/] ",
    "mdx": "[red][/] ",
    "markdown": "[red][/] ",
    "rmd": "[red][/] ",
    "rst": "[white][/] ",
    "tex": "[white][/] ",
    "texi": "[white][/] ",
    "texinfo": "[white][/] ",
    "zip": "[green][/] ",
    "tar": "[green][/] ",
    "gz": "[green][/] ",
    "bz2": "[green][/] ",
    "xz": "[green][/] ",
    "7z": "[green][/] ",
    "rar": "[green][/] ",
}

patterns = {
    ".*jquery.*.js$": " ",
    ".*angular.*.js$": " ",
    ".*backbone.*.js$": " ",
    ".*require.*.js$": " ",
    ".*materialize.*.js$": " ",
    ".*materialize.*.css$": " ",
    ".*mootools.*.js$": " ",
    ".*\.lock$": "󱧉 ",
}

exact = {
    "exact-match-case-sensitive-1.txt": "1",
    "exact-match-case-sensitive-2": "2",
    "gruntfile.coffee": " ",
    "gruntfile.js": " ",
    "gruntfile.ls": " ",
    "gulpfile.coffee": " ",
    "gulpfile.js": " ",
    "gulpfile.ls": " ",
    "mix.lock": "[magenta][/] ",
    "dropbox": "  ",
    ".ds_store": "[white][/] ",
    ".gitconfig": "[white][/] ",
    ".gitignore": "[white][/] ",
    ".gitlab-ci.yml": " ",
    ".bashrc": "[white][/] ",
    ".zshrc": "[white][/] ",
    ".vimrc": "[green4][/] ",
    ".gvimrc": "[green4][/] ",
    "_vimrc": "[green4][/] ",
    "_gvimrc": "[green4][/] ",
    ".bashprofile": "[white][/] ",
    "favicon.ico": "[yellow][/] ",
    "license": "[yellow][/] ",
    "node_modules": "[red][/] ",
    "react.jsx": "[cyan][/] ",
    "procfile": " ",
    "dockerfile": "[blue][/] ",
    "docker-compose.yml": "[blue][/] ",
    "makefile": "[white][/] ",
    "cmakelists.txt": "[white][/] ",
}

home_dirs = {
    "Desktop": " ",
    "Documents": " ",
    "Downloads": " ",
    "Music": " ",
    "Pictures": " ",
    "Games": "󱎓 ",
    "Videos": " ",
    "Public": " ",
}

# Initialize a Rich console
console = Console()


def sizeof_fmt(num, suffix="B"):
    # Define colors for each unit
    colors = {
        "": "white",  # Bytes
        "K": "bold white",  # Kilobytes
        "M": "yellow",  # Megabytes
        "G": "dim red",  # Gigabytes
        "T": "red",  # Terabytes
        "P": "red",  # Petabytes
        "E": "red",  # Exabytes
        "Z": "red",  # Zettabytes
        "Y": "red",  # Yottabytes
    }

    for unit in colors.keys():
        if abs(num) < 1024.0:
            color = colors[unit]
            return f"[{color}]{num:3.1f} {unit}{suffix}[/]"
        num /= 1024.0
    return f"[{colors['Y']}]{num:.1f}Yi{suffix}[/]"


def format_date(timestamp, format="%a %b %d %H:%M:%S %Y"):
    date = datetime.fromtimestamp(timestamp)
    date_str = date.strftime(format)
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    if date.strftime("%Y-%m-%d") == today_str:
        return f"[green]{date_str}"
    elif date.strftime("%Y-%m-%d") == yesterday_str:
        return f"[dim green]{date_str}"
    else:
        return f"[dim white]{date_str}"


def permissions_to_rich_text(permissions):
    permission_colors = {
        "d": "blue",  # Directory
        "r": "green",  # Read permission
        "w": "yellow",  # Write permission
        "x": "red",  # Execute permission
        "l": "cyan",  # Symbolic link
        "s": "bright_red",  # Socket
        "p": "bright_yellow",  # Pipe
        "c": "bright_green",  # Character device
        "b": "bright_blue",  # Block device
        "t": "bright_magenta",  # Named pipe
        "u": "dim white",  # No user
        "-": "dim white",  # No permission
    }
    rich_text = "".join(
        [f"[{permission_colors.get(char, 'white')}]{char}[/]" for char in permissions]
    )
    return rich_text


def get_entry_icon(entry_name, is_directory=False):
    if is_directory:
        default_dir_icon = " "
        if entry_name in home_dirs:
            return home_dirs[entry_name]
        else:
            return default_dir_icon

    for key, value in exact.items():
        if key == entry_name:
            return value

    for key, value in patterns.items():
        if re.match(key, entry_name):
            return value

    for key, value in extensions.items():
        entry_ext = entry_name.split(".")[-1] if "." in entry_name else ""
        if entry_ext == key:
            return value

    return " "


def calculate_directory_sizes(dir_entries, path, show_all, quiet):
    directory_sizes = {}

    if not quiet:
        progress = Progress(console=console, transient=True)
        with progress:
            task_id = progress.add_task(
                "[green]Calculating sizes...", total=len(dir_entries), visible=True
            )
            for dir_entry in dir_entries:
                dir_path = os.path.join(path, dir_entry)
                progress.update(
                    task_id,
                    description=f"[green]Calculating size of {dir_entry}...",
                    advance=1,
                )
                directory_sizes[dir_entry] = get_dir_size(
                    dir_path, show_all, progress, task_id, quiet
                )

    else:
        for dir_entry in dir_entries:
            dir_path = os.path.join(path, dir_entry)
            directory_sizes[dir_entry] = get_dir_size(
                dir_path, show_all, None, None, quiet
            )

    return directory_sizes


def get_dir_size(dir_path, show_all, progress, task_id, quiet):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        if not show_all:
            filenames = [f for f in filenames if not f.startswith(".")]
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size


def get_row_data(entry, path, options, directory_sizes=None):
    entry_path = os.path.join(path, entry)
    is_dir = os.path.isdir(entry_path)
    try:
        stat_info = os.lstat(entry_path)
        permissions = permissions_to_rich_text(stat.filemode(stat_info.st_mode))
        links = str(stat_info.st_nlink) if options["show_links"] else ""

        # Handling size for directories and files differently
        size = "[dim white]-[/]"
        if is_dir and options["show_folder_size"]:
            size = sizeof_fmt(directory_sizes.get(entry, 0))
        elif not is_dir:
            size = sizeof_fmt(stat_info.st_size)

        owner = getpwuid(stat_info.st_uid).pw_name if options["show_owner"] else ""
        group = getgrgid(stat_info.st_gid).gr_name if options["show_group"] else ""
        created = format_date(stat_info.st_ctime) if options["show_created"] else ""
        modified = format_date(stat_info.st_mtime) if options["show_modified"] else ""

        # Check if the file is executable, not a directory, and set color accordingly
        is_executable = os.access(entry_path, os.X_OK) and not is_dir
        entry_color = (
            "bold green" if is_executable else ("bold blue" if is_dir else "default")
        )
        entry_display = f"'{entry}'" if " " in entry else entry
        entry_display = f"[{entry_color}]{get_entry_icon(entry, is_dir)}{entry_display}"

        # Construct and return the row data, including a 'name' key for sorting by name
        return {
            "permissions": permissions,
            "links": links,
            "legible_size": size,
            "owner": owner,
            "group": group,
            "created": created,
            "modified": modified,
            "display_name": entry_display,
            "name": entry,
            "size": (
                directory_sizes.get(entry, 0)
                if is_dir and options["show_folder_size"]
                else stat_info.st_size
            ),
            "is_dir": is_dir,
        }
    except FileNotFoundError:
        # Handle missing files gracefully
        return None


def list_directory(
    path=".",
    table_format=False,
    show_header=False,
    sort_by=None,
    show_created=False,
    show_modified=False,
    show_all=False,
    show_links=False,
    show_size=False,
    show_permissions=False,
    show_owner=False,
    show_group=False,
    show_folder_size=False,
    reverse_sorting=False,
    quiet=False,
):
    if (
        show_header
        or sort_by
        or show_created
        or show_modified
        or show_size
        or show_permissions
        or show_owner
        or show_group
        or show_folder_size
        or reverse_sorting
    ):
        table_format = True

    if sort_by is None:
        sort_by = "name"

    entries = [
        entry for entry in os.listdir(path) if show_all or not entry.startswith(".")
    ]

    options = {
        "show_created": show_created,
        "show_modified": show_modified,
        "show_all": show_all,
        "show_links": show_links,
        "show_size": show_size,
        "show_permissions": show_permissions,
        "show_owner": show_owner,
        "show_group": show_group,
        "show_folder_size": show_folder_size,
    }

    if table_format:
        table = Table(
            show_header=show_header,
            header_style="bold magenta",
            box=None,
            show_edge=False,
            show_lines=False,
        )
        columns = []

        if show_permissions:
            columns.append("Permissions")
        if show_links:
            columns.append("Links")
        if show_size:
            columns.append("Size")
        if show_owner:
            columns.append("Owner")
        if show_group:
            columns.append("Group")
        if show_created:
            columns.append("Created")
        if show_modified:
            columns.append("Modified")
        columns.append("Name")

        for column in columns:
            table.add_column(
                column, justify="right" if column in ["Size", "Links"] else "left"
            )

        dir_entries = [
            entry for entry in entries if os.path.isdir(os.path.join(path, entry))
        ]
        directory_sizes = (
            calculate_directory_sizes(dir_entries, path, show_all, quiet)
            if show_folder_size
            else {}
        )

        rows_data = []
        for entry in entries:
            row_data = get_row_data(
                entry, path, options, directory_sizes=directory_sizes
            )
            if row_data:
                rows_data.append(row_data)

        def custom_sort(row):
            if sort_by == "size":
                if show_folder_size:
                    return -row["size"]
                else:
                    return (
                        not row["is_dir"] if reverse_sorting else row["is_dir"],
                        -row["size"],
                    )
            return row[sort_by].lower()

        rows_data.sort(key=custom_sort, reverse=reverse_sorting)

        for row_data in rows_data:
            data_to_add = []
            if show_permissions:
                data_to_add.append(row_data["permissions"])
            if show_links:
                data_to_add.append(row_data["links"])
            if show_size:
                data_to_add.append(row_data["legible_size"])
            if show_owner:
                data_to_add.append(row_data["owner"])
            if show_group:
                data_to_add.append(row_data["group"])
            if show_created:
                data_to_add.append(row_data["created"])
            if show_modified:
                data_to_add.append(row_data["modified"])
            data_to_add.append(row_data["display_name"])
            table.add_row(*data_to_add)

        console.print(table)
    else:
        for entry in entries:
            entry_path = os.path.join(path, entry)
            is_dir = os.path.isdir(entry_path)
            is_executable = os.access(entry_path, os.X_OK) and not is_dir
            entry_color = (
                "bold green"
                if is_executable
                else ("bold blue" if is_dir else "default")
            )
            entry_display = f"'{entry}'" if " " in entry else entry
            entry_display = (
                f"[{entry_color}]{get_entry_icon(entry, is_dir)}{entry_display}"
            )
            console.print(f"[{entry_color}]{entry_display}", end="  ")
        console.print()


parser = argparse.ArgumentParser(
    description="List files and directories with options for sorting, showing hidden ones, and coloring."
)

parser.add_argument(
    "path",
    nargs="?",
    default=".",
    help="Path for listing (default is the current directory).",
)
parser.add_argument(
    "-t", "--table", action="store_true", help="Use a table listing format."
)
parser.add_argument(
    "-H", "--show-header", action="store_true", help="Show table header."
)
parser.add_argument(
    "-a", "--all", action="store_true", help="Include hidden files and directories."
)
parser.add_argument(
    "-s",
    "--sort-by",
    choices=["name", "size", "created", "modified"],
    help="Sort by name (default), size, creation date, or modification date.",
)
parser.add_argument(
    "-c",
    "--show-created",
    action="store_true",
    help="Show creation date of files and directories.",
)
parser.add_argument(
    "-m",
    "--show-modified",
    action="store_true",
    help="Show last modification date of files and directories.",
)
parser.add_argument(
    "-n",
    "--show-links",
    action="store_true",
    help="Show number of links to files and directories.",
)
parser.add_argument(
    "-b", "--show-size", action="store_true", help="Show size of files and directories."
)
parser.add_argument(
    "-p",
    "--show-permissions",
    action="store_true",
    help="Show permissions of files and directories.",
)
parser.add_argument(
    "-u",
    "--show-owner",
    action="store_true",
    help="Show owner of files and directories.",
)
parser.add_argument(
    "-g",
    "--show-group",
    action="store_true",
    help="Show group of files and directories.",
)
parser.add_argument(
    "-x",
    "--show-folder-size",
    action="store_true",
    help="Show total size of directories.",
)
parser.add_argument(
    "-r", "--reverse-sorting", action="store_true", help="Reverse the sorting order."
)
parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="Suppress progress bars and other non-essential output",
)

args = parser.parse_args()

list_directory(
    path=args.path,
    table_format=args.table,
    show_header=args.show_header,
    sort_by=args.sort_by,
    show_created=args.show_created,
    show_modified=args.show_modified,
    show_all=args.all,
    show_links=args.show_links,
    show_size=args.show_size,
    show_permissions=args.show_permissions,
    show_owner=args.show_owner,
    show_group=args.show_group,
    show_folder_size=args.show_folder_size,
    reverse_sorting=args.reverse_sorting,
    quiet=args.quiet,
)
