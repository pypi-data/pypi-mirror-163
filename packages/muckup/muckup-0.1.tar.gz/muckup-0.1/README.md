# muckup

A simple backup utility built with Python and [Click](https://click.palletsprojects.com/en/8.1.x/).

## Installation
`pip install muckup`
<br>
or
<br>
`git clone https://github.com/manorajesh/pyty.git`
<br>
`pip install -r requirements.txt`
<br>
`bin/muckup`

## Usage
`muckup [-dntHi] SOURCE DESTINATION`
<br>
Simply type in the source path (can be relative) and destination path (can also be relative). The script will copy everything in the source (or the entire file) and copy it to the destination with the default name (`backup-%Y-%m-%d_%H:%M:%S`). Note: when copying one file, the extension will __not__ be preserved.

### Command Option Help
`-d, --dry-run`: Run the command without actually copying or pasting files (use for testing purposes)
<br>
`-n, --name TEXT`: Change the default name from `backup` to any string
<br>
`-t, --timestamp`: Remove timestamp from the name
<br>
`-H`: Dereference symbolic links (i.e. copy files and/or folders pointed to by symbolic links)
<br>
`-i`: Request a `(y/n)` confirmation before preforming backup command (WIP)
<br>
`-g TEXT`: Change timestamp format using the [time.strftime directives](https://docs.python.org/3/library/time.html#time.strftime).
<br>
`-h, --help`: Show this message in shorter form.

<hr>

##### Contents of requirements.txt
`click==8.1.3`
