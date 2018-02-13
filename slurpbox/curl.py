import pycurl
import settings
from tqdm import tqdm

LOGIN = f'{settings.username}:{settings.password}'
BAR = None
BLAST = 0

def header_func(header_line):
    header_line = header_line.decode('iso-8859-1') # from spec
    print(header_line)

def progress(download_t, download_d, upload_t, upload_d):
    global BAR
    global BLAST

    if download_t == 0:
        return
    else:
        if BAR is None:
            BAR = tqdm(total=download_t, unit='B', unit_scale=True)

    # print(download_t, download_d)
    diff = download_d - BLAST
    BLAST = download_d
    # print(download_d, BLAST, diff)

    BAR.update(diff)

def PROPFIND(url_part, out_obj):
    url = settings.root_path + url_part

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, out_obj)
    # c.setopt(c.HEADERFUNCTION, header_func)
    # c.setopt(c.NOPROGRESS, False)
    # c.setopt(c.XFERINFOFUNCTION, progress)
    c.setopt(c.CUSTOMREQUEST, 'PROPFIND')
    c.setopt(c.USERPWD, LOGIN)
    #c.setopt(c.RANGE, '0-499')
    c.perform()
    c.close()

def download_file(url_part, out_obj):
    global BAR
    global BLAST

    url = settings.root_path + url_part
    # print(f"Downloading: {url}")

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, out_obj)
    # c.setopt(c.HEADERFUNCTION, header_func)
    c.setopt(c.NOPROGRESS, False)
    c.setopt(c.XFERINFOFUNCTION, progress)
    # c.setopt(c.CUSTOMREQUEST, 'PROPFIND')
    c.setopt(c.USERPWD, LOGIN)
    #c.setopt(c.RANGE, '0-499')
    c.perform()
    c.close()

    BAR.close()
    BLAST = 0
    BAR = None
