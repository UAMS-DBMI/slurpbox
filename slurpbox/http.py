import requests
from tqdm import tqdm

AUTH = None
BASEURL = None

CHUNK_SIZE = 1024 * 1024

def init(username, password, baseurl):
    global AUTH
    global BASEURL

    BASEURL = baseurl
    AUTH = (username, password)

def PROPFIND(url_part, out_obj):
    url = BASEURL + url_part

    response = requests.request('PROPFIND', url, auth=AUTH, stream=True)
    for chunk in response.iter_content(chunk_size=None):
        out_obj.write(chunk)


def download_file(url_part, out_obj):
    url = BASEURL + url_part

    response = requests.get(url, auth=AUTH, stream=True)

    size = int(response.headers.get('Content-Length', 0))

    bar = tqdm(total=size, unit='B', unit_scale=True)

    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        out_obj.write(chunk)
        bar.update(len(chunk))
    
