# wafiq's comment
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib import parse
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm


websitename = "https://www.mangareader.net/"
# series_url = input("Enter full URL of desired series: ")


def write_to_zip(image, num, zf):
    with zf.open(f"{num:03}.jpg", "w") as zfile:
        zfile.write(image)


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
    base_url = "https://www.mangareader.net/{}"

    def __init__(self, name):
        self._chapter_list = None
        self.name = name.replace("-", " ")
        super().__init__(self.base_url.format(name))

    def enumerate_chapters(self):
        chapters = self.soup.select("div#chapterlist a")
        return [
            parse.urljoin(websitename, chapter.attrs["href"])
            for chapter in chapters
        ]

    def download(self, latest):
        chapters = self.chapters()
        chapters = chapters[-latest:] if latest is not None else chapters
        self.create_folder()
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = [pool.submit(chap.download) for chap in chapters]
            for result in tqdm(
                as_completed(results),
                total=len(results),
                desc="Chapter progress",
            ):
                pass

    def create_folder(self): 
        if not os.path.exists(self.name): 
            os.mkdir(self.name)   
    # def build_directory(self):
    #    return os.mkdir(nameofmanga)

    @property
    def chapter_list(self):
        if self._chapter_list is None:
            self._chapter_list = self.enumerate_chapters()
        return self._chapter_list

    def generate_chapter(self, url):
        return Chapter(url)

    def chapters(self):
        return [self.generate_chapter(ch) for ch in self.chapter_list]


class Chapter(WebPage):
    def __init__(self, url):
        self._page_list = None
        super().__init__(url)

    def enumerate_pages(self):
        pages = self.soup.select("div#selectpage option")
        return [
            parse.urljoin(websitename, page.attrs["value"]) for page in pages
        ]

    def download(self) -> None:
        zf_name = f"{self.series}/Ch.{self.number}.cbz"
        with ZipFile(zf_name, "w") as zf:
            with ThreadPoolExecutor(max_workers=8) as pool:
                results = [
                    pool.submit(page.download, num)
                    for num, page in enumerate(self.pages())
                ]
                for result in tqdm(
                    as_completed(results),
                    total=len(results),
                    leave=False,
                    desc=zf_name,
                ):
                    image, num = result.result()
                    write_to_zip(image, num, zf)

    @property
    def info(self):
        return re.search(r".*/(?P<series>[^/]*)/(?P<num>\d*)", self.url)

    @property
    def number(self):
        num = int(self.info["num"])
        return f"{num:03}"

    @property
    def series(self):
        # return self.info["series"]
        return self.info["series"].replace("-", " ")

    @property
    def page_list(self):
        if self._page_list is None:
            self._page_list = self.enumerate_pages()
        return self._page_list

    def generate_page(self, url):
        return Page(url)

    def pages(self):
        return [self.generate_page(p) for p in self.page_list]


class Page(WebPage):
    def download(self, num: int) -> (bytes, int):
        """A download image function 
        Args: 
            num (int): The page number for the future write, due to threads 
             
        Returns: 
            (bytes, int): The bytes for the image, from Response.content 
        """
        resp = requests.get(self.image)
        return resp.content, num

    @property
    def image(self):
        img = self.soup.find("img", id="img")
        return img.attrs["src"]
