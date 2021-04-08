import re
from . import base
import cfscrape
import cookiejar

class WebPage(base.WebPage):
   def __init__(self,url):
       self._scraped = None
       self._jar = None
       self._soup = None
       self._url = url

       @property
       def scraped(self):
           scraper = cfscraper.Cloudflarescraper()
           if self._scraped is None:
               self._scraped = scraper.get(url).content

        @property
        def soup(self):
        if self._soup is None:
            self._soup = BS(self._scraped.text, "html.parser")
        return self._soup

class Series(base.Series):
    base_url = "https://readcomiconline.to/Comic/{}"
    tags = ["readcomiconline", "rco"]

    def enumerate_chapters(self):
        chapters = self.soup.select("div.section group a")
        return [chapter.attrs["href"] for chapter in chapters[::-1]]

    def generate_chapter(self, url):
        return Chapter(url)


class Chapter(base.Chapter):
    def enumerate_pages(self):
        pages = self.soup.select("div.divImage img")
        return [page["src"] for page in pages]

    @property
    def info(self):
        return re.search(
            r".*/Comic/(?P<series>[^/]*)/Issue-(?P<num>\d*)", self.url
        )

    def generate_page(self, url):
        return Page(url)


class Page(base.Page):

    @property
    def image(self):
        pass
