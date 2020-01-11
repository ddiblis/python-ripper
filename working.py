# wafiq's comment

from bs4 import BeautifulSoup as BS
import requests
from tqdm import tqdm
from zipfile import ZipFile
import os.path
from urllib.parse import urlparse
from urllib import parse

websitename = "https://www.mangareader.net/"
chapter_url = "https://www.mangareader.net/goblin-is-very-strong/18"

output = urlparse(chapter_url).path

for splitoutput in output:
    splitpath = os.path.split(output) 
    serieswithslash = splitpath[0].split("/") 
    series = serieswithslash[1] 
    chapter_number = splitpath[1] 

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


class Page(WebPage):
    @property
    def image(self):
        img = self.soup.find("img", id="img")
        return img.attrs["src"]


class Chapter(WebPage):
    def __init__(self, url):
        self._page_list = None
        super().__init__(url)

    def enumerate_pages(self):
        pages = self.soup.select("div#selectpage option")
        return [
            parse.urljoin(websitename, page.attrs["value"]) for page in pages
        ]

    def generate_page(self, url):
        return Page(url)

    def download(self, ): 
        pages = self.pages()
        with ZipFile(f"{series}  {chapter_number} .cbz", "w") as zf:     
             for num, p in tqdm(enumerate(pages, 1), total=len(pages), desc=f"text"): 
                 with zf.open(f"{series}  {chapter_number} {num:02}.jpg", "w") as f: 
                     resp = requests.get(p.image) 
                     f.write(resp.content) 

    @property
    def page_list(self):
        if self._page_list is None:
            self._page_list = self.enumerate_pages()
        return self._page_list
    
    def pages(self):
        return [self.generate_page(p) for p in self.page_list]


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
