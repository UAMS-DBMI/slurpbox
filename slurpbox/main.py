#!/usr/bin/env python3

from io import BytesIO
import os
from pathlib import Path
from typing import NamedTuple
import argparse

from .xmlparse import process_xml
from .hash import sha1sum_from_file
from .util import format_sizeof
from .curl import PROPFIND, download_file, init_curl

from .settings import SETTINGS, load_settings_file, NoConfigFoundError, settings_to_namespace
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

    choice = input("\nPlease enter folder choice (or q to abort): ")

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
    return set(files)

def print_file_report(folder, files):

    files_size = format_sizeof(sum([f.size for f in files]), 'B')
    files_count = len(files)
    files_head = list(files)[:5]

    print(f"This folder contains {files_count} new files, which will "
          f"consume {files_size}.")
    print("Here are the first few files:")
    for file in files_head:
        file_size = format_sizeof(file.size, 'B')
        print(f"    {file_size}\t{file.path}")

    print("    ....\t....")

def filter_existing_files(files, verify=True):
    print("Checking for existing files...")
    existing_files = []
    incorrect_files = []

    for file in files:
        test_filename = DESTINATION / os.path.basename(file.path)
        if os.path.exists(test_filename):
            if verify:
                print(f"\tVerifying {test_filename}...")
                if verify_file(test_filename, file.etag):
                    existing_files.append(file)
                else:
                    incorrect_files.append(file)
            else:
                existing_files.append(file)
                
    if len(incorrect_files) > 0:
        # TODO: print a report of what those files are
        print("\nSome of the files you wish to download already exist "
              "in your destination directory, however their sha1 checksum "
              "does not match what Box has.")

        print("\nThis may indicate a failed partial download, or it could be "
              "completely different files with the same name.")

        print("\nYou must provide input on how these files should be handled. "
              "If you answer Yes, the exsiting files will be DELETED and "
              "replaced with the contents on Box. If you answer No, "
              "the existing files will be left in place, and the copies on "
              "Box WILL NOT be downloaded.")

        choice = input("\nWould you like to overwrite these files? [y/N] ")
        if choice.upper() == 'N' or choice == '':
            # If the user DOES NOT want to overwrite exsiting partial
            # downloads, consider them "existing files" so they are
            # excluded from the download set.
            existing_files.extend(incorrect_files)

    return set(existing_files)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Download all files from a Box.com directory',
        # Add more text here
        epilog='Arguments take precedence over configuration files.',
    )

    parser.add_argument("-x", "--no-config", action="store_true",
                        help="ignore any config files")

    parser.add_argument(
        "-n", "--no-verify", action="store_true",
        help="do not verify existing local files, assume they are correct"
    )

    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="do not ask if you are sure, download everything"
    )

    parser.add_argument(
        "--username", '-u',
        help="your Box.com username"
    )
    parser.add_argument(
        "--password", '-p',
        help="your Box.com password"
    )
    parser.add_argument(
        "--remote-path", '-r',
        help="remote path, from which all files will be downloaded"
    )
    parser.add_argument(
        "--local-path", '-l',
        help="local path, to which all downloaded files will be saved"
    )

    args = settings_to_namespace(SETTINGS)

    parser.parse_args(namespace=args)

    return args

def verify_config(args):
    valid = True
    error_message = \
        "Error: {} must be specified in config file or via arguments!"

    if args.username is None:
        valid = False
        print(error_message.format("username"))
    if args.password is None:
        valid = False
        print(error_message.format("password"))
    if args.local_path is None:
        valid = False
        print(error_message.format("local path (destination)"))

    if not valid:
        print(config_file_help)
        return False
    else:
        return True

def main(args=None):
    global DESTINATION

    no_config = False

    try:
        load_settings_file()
    except NoConfigFoundError:
        no_config = True

    args = parse_args()

    # Ignore missing config if -x is passed
    if args.no_config:
        no_config = False

    if no_config:
        print("No configuration file found!")
        print(config_file_help)
        return 1

    if not verify_config(args):
        return 1

    print(f"""
Slrupbox 1.1 - A tool for downloading files from Box.

Configuration:
    Box user: {args.username}
    Destination directory: {args.local_path}

""")

    DESTINATION = Path(args.local_path)

    # TODO: adjust this to be prettier
    init_curl(args.username,
              args.password,
              "https://dav.box.com/")  # hardcoded root_path for now

    if args.remote_path is None:
        folder = choose_folder()
    else:
        folder = args.remote_path

    print(f"\nYou have chosen: {folder}")

    files = get_files(folder)

    existing_files = filter_existing_files(files, verify=(not args.no_verify))
    files_to_download = files.difference(existing_files)

    if len(files_to_download) > 0:
        print_file_report(folder, files_to_download)
    else:
        print("There are no new files to download!")
        return 0


    if args.yes:
        choice = 'Y'
    else:
        choice = input("\nWould you like to continue? [Y/n] ")

    if choice.upper() == 'Y' or choice == '':
        download_files(files_to_download)

    # TODO: print a report of what was done

    return 0

if __name__ == '__main__':
    main()
