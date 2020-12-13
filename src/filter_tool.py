import re
import requests
from lxml import html

def find_url(string):
    codes = []

    # nhentai handler
    nhentai_regex = r"(?i)\b(?:https?://nhentai.net/g/\d+|www\d{0,3}[.]nhentai.net/g/\d+|nhentai.net/g/\d+)"
    nhentai_url = re.findall(nhentai_regex,string)
    for i in nhentai_url:
        if i[-1] == '/':
            codes.append('https://nhentai.net/api/gallery/{}'.format(i.split('/')[-2]))
        else:
            codes.append('https://nhentai.net/api/gallery/{}'.format(i.split('/')[-1]))

    # hentai2read handler
    hentai2read_regex = r"(?i)\b(?:https?://hentai2read.com/[a-zA-Z0-9_]*|www\d{0,3}[.]hentai2read.com/[a-zA-Z0-9_]*|hentai2read.com/[a-zA-Z0-9_]*)"
    hentai2read_url = re.findall(hentai2read_regex,string)
    for i in hentai2read_url:
        codes.append(i)

    return codes

def scan_links(urls, channel_name, censoredtags):
    clean = False
    problemmatic_tags = []
    if channel_name in censoredtags.keys():
        additional = censoredtags[channel_name]
    else:
        additional = []
    list_of_tags = censoredtags['all'] + additional
    for link in urls:
        page = requests.get(link)
        if page.ok:
            if 'nhentai' in link: # nhentai filterer
                tags = page.json()["tags"]
                for tag in tags:
                    if tag["name"] in list_of_tags:
                        clean = True
                        problemmatic_tags.append(tag["name"])
            elif 'hentai2read' in link: # hentai2read filterer
                tree = html.fromstring(page.content)
                tags = tree.xpath('//a[@class="tagButton"]/text()')
                for tag in tags:
                    if tag in list_of_tags:
                        clean = True
                        problemmatic_tags.append(tag)

    return clean, problemmatic_tags