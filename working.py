from bs4 import BeautifulSoup as BS
import requests
from urllib import parse

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
            self._soup = BS(self.resp.text) 
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
        return [parse.urljoin(websitename, page.attrs["value"])  for page in pages]
    def generate_page(self, url):
        return Page(url)
    @property
    def page_list(self):
        if self._page_list is None:
            self._page_list = self.enumerate_pages()
        return self._page_list
