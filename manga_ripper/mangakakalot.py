import re
from . import base


class Series(base.Series):
    base_url = "https://mangakakalot.com/manga/{}"
    tags = ["mangakakalot", "mk"]

    def enumerate_chapters(self):
        chapters = self.soup.select("div#chapter a")
        return [chapter.attrs["href"] for chapter in chapters[::-1]]

    def generate_chapter(self, url):
        return Chapter(url)


class Chapter(base.Chapter):
    def enumerate_pages(self):
        pages = self.soup.select("div.vung-doc img")
        return [page["src"] for page in pages]

    @property
    def info(self):
        return re.search(
            r".*/(?P<series>[^/]*)/chapter_(?P<num>\d*)", self.url
        )

    def generate_page(self, url):
        return Page(url)


class Page(base.Page):
    def __init__(self, img):
        self._image = img

    @property
    def image(self):
        return self._image
