import re
from . import base
import cfscrape

class WebPage(base.WebPage):
    pass
    
class Series(base.Series):
    base_url = "https://mangadog.club/read/{}"
    tags = ["mangadog", "mgd"]

    def enumerate_chapters(self):
        chapters = self.soup.select(".chapter-title-rtl\ text-left a")
        return [chapter.attrs["href"] for chapter in chapters[::-1]]

    def generate_chapter(self, url):
        return Chapter(url)


class Chapter(base.Chapter):
    def enumerate_pages(self):
        pages = self.soup.select(".img-responsive img")
        return [page["src"] for page in pages]

    @property
    def info(self):
        return re.search(
            r".*/read/(?P<series>[^/]*)/chapter-(?P<num>\d*)", self.url
        )

    def generate_page(self, url):
        return Page(url)


class Page(base.Page):

    @property
    def image(self):
        pass
