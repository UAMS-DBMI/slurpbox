config_file_help = """
Slurpbox looks for its configuration first in the current directory (named
slurpbox.conf), then in the current user's home directory (named .slurpboxrc),
and finally in the default system location, /etc/slurpbox/slurpbox.conf.

The config file is a YAML file, which should take the following form:

# slurpbox.conf

remote:
    username: <username@host>
    password: <password>

    # The root WebDAV address; you probably don't want to change this
    root_path: https://dav.box.com/

local:
    # Where to store downloaded files
    destination: <location>
"""
