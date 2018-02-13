import yaml
from os.path import exists, expanduser
from pprint import pprint


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

    raise RuntimeError("No configuration file found")


def load_config():
    with open(find_config()) as inf:
        return yaml.load(inf)


SETTINGS = load_config()
