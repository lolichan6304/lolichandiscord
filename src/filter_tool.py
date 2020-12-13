import re
import requests
from lxml import html

from src.extensions.web_extensions import *

def find_url(string):
    codes = []

    # nhentai handler
    codes += Nhentai().find_links(string)

    # hentai2read handler
    codes += Hentai2read().find_links(string)

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
        if 'nhentai' in link: # nhentai filterer
            tags = Nhentai().get_tags(link)

        elif 'hentai2read' in link: # hentai2read filterer
            tags = Hentai2read().get_tags(link)

        # search for tags in list_of_tags
        if tags is not None:
            for tag in tags:
                if tag in list_of_tags:
                    clean = True
                    problemmatic_tags.append(tag)

    return clean, problemmatic_tags