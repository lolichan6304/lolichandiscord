import re
import requests
from lxml import html

class Nhentai:

    # constructor
    def __init__(self):
        self.regex = regex = r"(?i)\b(?:https?://nhentai.net/g/\d+|www\d{0,3}[.]nhentai.net/g/\d+|nhentai.net/g/\d+)"

    def find_links(self, message):
        self.codes = []
        urls = re.findall(self.regex, message)
        for i in urls:
            if i[-1] == '/':
                self.codes.append('https://nhentai.net/api/gallery/{}'.format(i.split('/')[-2]))
            else:
                self.codes.append('https://nhentai.net/api/gallery/{}'.format(i.split('/')[-1]))
        return self.codes

    def get_tags(self, url):
        page = requests.get(url)
        if page.ok:
            tags = page.json()["tags"]
            return [x["name"].lower() for x in tags]
        else:
            return None


class Hentai2read:

    # constructor
    def __init__(self):
        self.regex = regex = r"(?i)\b(?:https?://hentai2read.com/[a-zA-Z0-9_]*|www\d{0,3}[.]hentai2read.com/[a-zA-Z0-9_]*|hentai2read.com/[a-zA-Z0-9_]*)"

    def find_links(self, message):
        self.codes = []
        url = re.findall(self.regex, message)
        for i in url:
            codes.append(i)
        return self.codes

    def get_tags(self, url):
        page = requests.get(url)
        if page.ok:
            tree = html.fromstring(page.content)
            tags = tree.xpath('//a[@class="tagButton"]/text()')
            return [x.lower() for x in tags]