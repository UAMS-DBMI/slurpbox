import requests
from tqdm import tqdm

from .settings import SETTINGS


def propfind(url_part, out_obj):
    """Perform an HTTP PROPFIND on the given url, storing in out_obj

    PROPFIND is part of WebDAV, and should return (in XML) a set of
    properties about the given resource.

    In the case of Box.com, they require use of PROPFIND for 
    directory listings, as well as for getting details about an
    individual file.
    """

    url = SETTINGS['remote']['root_path'] + url_part

    r = requests.request('PROPFIND',
                         url,
                         auth=(SETTINGS['remote']['username'],
                               SETTINGS['remote']['password']))
    out_obj.write(r.content)

def download_file(url_part, out_obj):
    """Download a file from the given url, storing in out_obj"""

    url = SETTINGS['remote']['root_path'] + url_part

    r = requests.get(url, 
                     stream=True,
                     auth=(SETTINGS['remote']['username'],
                           SETTINGS['remote']['password']))

    content_length = int(r.headers['content-length'])
    progress_bar = tqdm(total=content_length, unit='B', unit_scale=True)

    for chunk in r.iter_content(chunk_size=1024): 
        if chunk: # filter out keep-alive new chunks
            out_obj.write(chunk)
            progress_bar.update(1024)
    progress_bar.close()
