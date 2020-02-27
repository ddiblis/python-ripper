import re
from . import base


class Series(base.Series):
    base_url = "https://viewcomics.net/comic/{}"
    tags = ["viewcomics", "vc"]

    def enumerate_chapters(self):
        chapters = self.soup.select(".basic-list a")
        return [chapter.attrs["href"] for chapter in chapters[::-1]]

    def generate_chapter(self, url):
        return Chapter(url)


class Chapter(base.Chapter):
    def enumerate_pages(self):
        pages = self.soup.select(".full-select option")
        return [page["value"] for page in pages]

    @property
    def info(self):
        return re.search(r".*/(?P<series>[^/]*)/issue-(?P<num>\d*)", self.url)

    def generate_page(self, url):
        return Page(url)


class Page(base.Page):

    @property
    def image(self):
        img = self.soup.select("div.chapter-container img")[0]
        return img.attrs["src"]

