import pycurl
from tqdm import tqdm

LOGIN = None
BASEURL = None
BAR = None
BLAST = 0

def init_curl(username, password, base_url):
    global LOGIN, BASEURL
    LOGIN = ':'.join([
        username,
        password,
    ])
    BASEURL = base_url


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

    # BAR.update(n) expects n to be the number of bytes since
    # we last called it, however download_d is the total number of bytes
    # downloaded, so we need to adjust it..
    diff = download_d - BLAST
    BLAST = download_d

    BAR.update(diff)

def PROPFIND(url_part, out_obj):
    url = BASEURL + url_part

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

    url = BASEURL + url_part

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
