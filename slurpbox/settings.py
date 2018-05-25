import yaml
import argparse
from os.path import exists, expanduser
from pprint import pprint

class NoConfigFoundError(RuntimeError):
    pass

SETTINGS = {}

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

    with open(filename) as inf:
        SETTINGS.update(yaml.load(inf))

# TODO: if we change the yaml file to be flat, 
#       we could get rid of this entirely (I think?)
def settings_to_namespace(settings):
    """Flatten the given settings dict into a simple Namespace object"""
    ns = argparse.Namespace()
    try:
        ns.username = settings['remote']['username']
        ns.password = settings['remote']['password']
        ns.root_path = settings['remote']['root_path']
        ns.local_path = settings['local']['destination']
    except:
        pass

    return ns
