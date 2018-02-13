from lxml import etree


def process_prop(prop):
    def fix_name(name):
        return name.replace('{DAV:}', '')

    ret = {}
    for i in prop:
        ret[fix_name(i.tag)] = i.text

    return ret

def process_response(response):
    filename = None
    for i in response.iter("{DAV:}href"):
        filename = i.text

    for p in response.iter("{DAV:}prop"):
        ret = process_prop(p)

    ret['filename'] = filename
    return ret


def process_xml(xml_data):
    # tree = etree.parse('dirlist.xml')
    root = etree.fromstring(xml_data)

    # root = tree.getroot()

    ret = []
    for i in root.iter("{DAV:}response"):
        ret.append(process_response(i))

    return ret

if __name__ == '__main__':
    from pprint import pprint

    with open('dirlist.xml', 'rb') as f:
        pprint(process_xml(f.read()))
