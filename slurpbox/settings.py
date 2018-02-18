import configparser
from os.path import exists, expanduser
from pprint import pprint

class NoConfigFoundError(RuntimeError):
    pass

SETTINGS = configparser.ConfigParser()

def find_config():
    paths = [
        './slurpbox.conf',
        '~/.slurpboxrc',
        '/etc/slurpbox/slurpbox.conf',
    ]

    for path in paths:
        p = expanduser(path)
        if exists(p):
            return p

    raise NoConfigFoundError()


def load_settings_file(filename=None):
    global SETTINGS

    if filename is None:
        filename = find_config()

    SETTINGS.read(filename)
