# wafiq's comment
import re
from urllib import parse

from . import base


websitename = "https://www.mangareader.net/"

class Series(base.Series):
    base_url = "https://www.mangareader.net/{}"
    tags = ["mangareader", "mr"]

    def enumerate_chapters(self):
        chapters = self.soup.select("div#chapterlist a")
        return [
            parse.urljoin(websitename, chapter.attrs["href"])
            for chapter in chapters
        ]

    def generate_chapter(self, url):
        return Chapter(url)

class Chapter(base.Chapter):

    def enumerate_pages(self):
        pages = self.soup.select("div#selectpage option")
        return [
            parse.urljoin(websitename, page.attrs["value"]) for page in pages
        ]

    @property
    def info(self):
        return re.search(r".*/(?P<series>[^/]*)/(?P<num>\d*)", self.url)

    def generate_page(self, url):
        return Page(url)

class Page(base.Page):

    @property
    def image(self):
        img = self.soup.find("img", id="img")
        return img.attrs["src"]
