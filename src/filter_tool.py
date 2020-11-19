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

def scan_links(urls, censoredtags):
    problemmatic_tags = ["loli", "lolicon", "shotacon"]
    for link in urls:
        #page = requests.get('https://nhentai.net/api/gallery/{}'.format(link))
        page = requests.get('https://google.com')
        tree = html.fromstring(page.content)
    
    return True, problemmatic_tags