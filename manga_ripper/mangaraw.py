import re
from . import base
from urllib import parse


class Series(base.Series):
    base_url = "https://mangaraw.org/{}"
    tags = ["mangaraw", "mrw"]

    def __init__(self, name):
        self._chapter_list = None
        super().__init__(name)
        self.name = name.replace("_", " ")

    def enumerate_chapters(self):
        chapters = self.soup.select(".lchx a")
        return [chapter.attrs["href"] + "/" for chapter in chapters[::-1]]

    def generate_chapter(self, url):
        return Chapter(url)


class Chapter(base.Chapter):
    def enumerate_pages(self):
        pages = self.soup.select(".page-link option")
        half = int(len(pages) / 2)
        return [
            parse.urljoin(self.url, page["value"]) for page in pages[0:half]
        ]

    @property
    def series(self):
        return self.info["series"].replace("_", " ")

    @property
    def info(self):
        return re.search(r"org/(?P<series>[^/]*)/(?P<num>.*)/", self.url)

    def generate_page(self, url):
        return Page(url)


class Page(base.Page):

    @property
    def image(self):
        img = self.soup.find("img", class_="picture")
        return img.attrs["src"]
