import re
import requests
from lxml import html

def find_url(string):
    regex = r"(?i)\b(?:https?://nhentai.net/g/\d+|www\d{0,3}[.]nhentai.net/g/\d+|nhentai.net/g/\d+)"
    url = re.findall(regex,string)
    codes = []
    for i in url:
        if i[-1] == '/':
            codes.append(i.split('/')[-2])
        else:
            codes.append(i.split('/')[-1])
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
        page = requests.get('https://nhentai.net/api/gallery/{}'.format(link))
        tags = page.json()["tags"]
        for tag in tags:
            if tag["name"] in list_of_tags:
                clean = True
                problemmatic_tags.append(tag["name"])
    return clean, problemmatic_tags