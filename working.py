# wafiq's comment
import re
from urllib import parse
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

websitename = "https://www.mangareader.net/"
chapter_url = "https://www.mangareader.net/goblin-is-very-strong/18"


class WebPage:
    def __init__(self, url):
        self._resp = None
        self._soup = None
        self.url = url

    @property
    def resp(self):
        if self._resp is None:
            self._resp = requests.get(self.url)
        return self._resp

    @property
    def soup(self):
        if self._soup is None:
            self._soup = BS(self.resp.text, "html.parser")
        return self._soup


class Series(WebPage):
    def __init__(self, url):
        self._chapter_list = None
        super().__init__(url)

    def enumerate_chapters(self):
        chapters = self.soup.select("div#chapterlist a")
        return [
            parse.urljoin(websitename, chapter.attrs["href"])
            for chapter in chapters
        ]

    def generate_chapter(self, url):
        return Chapter(url)

    # def build_directory(self):
    #    return os.mkdir(nameofmanga)

    @property
    def chapter_list(self):
        if self._chapter_list is None:
            self._chapter_list = self.enumerate_chapters()
        return self._chapter_list


class Chapter(WebPage):
    def __init__(self, url):
        self._page_list = None
        super().__init__(url)

    def enumerate_pages(self):
        pages = self.soup.select("div#selectpage option")
        return [
            parse.urljoin(websitename, page.attrs["value"]) for page in pages
        ]

    def download(self,):
        pages = self.pages()
        with ZipFile(f"{self.series} Ch.{self.number}.cbz", "w") as zf:
            for num, p in tqdm(
                enumerate(pages, 1),
                total=len(pages),
                desc=f"{self.series} Ch.{self.number}",
            ):
                with zf.open(f"{num:03}.jpg", "w") as f:
                    resp = requests.get(p.image)
                    f.write(resp.content)

    @property
    def info(self):
        return re.search(r".*/(?P<series>[^/]*)/(?P<num>\d*)", self.url)

    @property
    def number(self):
        return self.info["num"]

    @property
    def page_list(self):
        if self._page_list is None:
            self._page_list = self.enumerate_pages()
        return self._page_list

    @property
    def series(self):
        return self.info["series"].replace("-", " ")

    def generate_page(self, url):
        return Page(url)

    def pages(self):
        return [self.generate_page(p) for p in self.page_list]


class Page(WebPage):
    @property
    def image(self):
        img = self.soup.find("img", id="img")
        return img.attrs["src"]
