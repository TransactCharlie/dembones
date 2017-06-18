import json
from urllib.parse import urljoin


class WebPage:
    """Models what's important to us about a web page"""
    title = None
    links = []
    images = []
    scripts = []

    def __init__(self, title=None, links=None, images=None, scripts=None):
        self.title = title
        self.links = [] if links is None else links
        self.images = [] if images is None else images
        self.scripts = [] if scripts is None else scripts

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_soup(cls, soup, url):
        """Return a WebPage from a BeautifulSoup Object"""
        links = [urljoin(url, l["href"]) for l in soup.find_all('a', href=True)]
        images = [urljoin(url, i["src"]) for i in soup.find_all('img', src=True)]
        scripts = [urljoin(url, s["src"]) for s in soup.find_all('script', src=True)]
        title = soup.title.string
        return cls(title=title, links=links, images=images, scripts=scripts)
