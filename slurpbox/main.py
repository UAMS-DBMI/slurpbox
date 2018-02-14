#!/usr/bin/env python3

from io import BytesIO
import os
from pathlib import Path
from typing import NamedTuple

from .xmlparse import process_xml
from .hash import sha1sum_from_file
from .util import format_sizeof
from .curl import PROPFIND, download_file, init_curl

from .settings import SETTINGS, load_settings_file, NoConfigFoundError
from .messages import config_file_help

DESTINATION = None


class File(NamedTuple):
    path: str
    etag: str
    size: int

def verify_file(full_path, etag):
    """Verify the given file is correct

    etag is an sha1sum, optionally enclosed in double quotes"""

    digest = etag.replace('"', '') # kill "'s
    sha1 = sha1sum_from_file(full_path)

    return sha1 == digest

def download_files(files):
    for file in files:
        if not try_a_hundred_times(file):
            raise Exception("Failed to download file")

def try_a_hundred_times(file):
    for t in range(1000):
        if download_and_verify(file):
            return True

    return False


def download_and_verify(file):
    full_filename = file.path
    short_filename = os.path.basename(full_filename)

    print(f"Downloading {short_filename}...")

    output_file = DESTINATION / short_filename
    with output_file.open('wb') as outf:
        download_file(full_filename, outf)

    return verify_file(output_file, file.etag)

def get_folders():
    buffer = BytesIO()
    PROPFIND('dav/', buffer)

    folders = []
    for item in process_xml(buffer.getvalue()):
        if item['filename'] == '/dav/':
            continue
        if 'getcontenttype' in item: # indicates a file
            continue

        folders.append(item['filename'])
    return folders


def choose_folder():
    folders = get_folders()
    for i, folder in enumerate(folders):
        print(f"{i}. {folder}")

    choice = input("\nPlease enter folder choice (or q to abort):")

    try:
        chosen = folders[int(choice)]
    except:
        exit()

    return chosen

def get_files(folder):
    buffer = BytesIO()
    PROPFIND(folder, buffer)

    files = []
    for item in process_xml(buffer.getvalue()):
        if 'getcontenttype' not in item: # indicates a folder
            continue

        files.append(File(item['filename'],
                          item['getetag'],
                          int(item['getcontentlength'])))
    return files

def print_file_report(folder, files):

    files_size = format_sizeof(sum([f.size for f in files]))
    files_count = len(files)
    files_head = files[:5]

    print(f"You have chosen: {folder}")
    print(f"This folder contains {files_count} files, which will "
          f"consume {files_size}.")
    print("Here are the first few files:")
    for file in files_head:
        file_size = format_sizeof(file.size)
        print(f"    {file_size}\t{file.path}")
    print("    ....\t....")


def main(args=None):
    global DESTINATION

    # TODO: parse arguments

    try:
        load_settings_file()
    except NoConfigFoundError:
        print("No configuration file found!")
        print(config_file_help)
        return 1

    DESTINATION = Path(SETTINGS['local']['destination'])

    # TODO: adjust this to be prettier
    init_curl(SETTINGS['remote']['username'],
              SETTINGS['remote']['password'])

    folder = choose_folder()

    files = get_files(folder)
    print_file_report(folder, files)

    choice = input("\nWould you like to continue? [Y/n]")

    if choice.upper() == 'Y' or choice == '':
        download_files(files)

    # TODO: print a report of what was done

    return 0

if __name__ == '__main__':
    main()
