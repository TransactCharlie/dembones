import aiohttp
from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urljoin
import json


STORE = {}


class WebPage:
    url = None
    title = None
    links = []
    images = []
    scripts = []

    def __init__(self, url=None, title=None, links=None, images=None, scripts=None):
        self.url = url
        self.title = title
        self.links = [] if links is None else links
        self.images = [] if images is None else images
        self.scripts = [] if scripts is None else scripts

    def __str__(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_soup(cls, soup, url):
        links = [urljoin(url, l["href"]) for l in soup.find_all('a', href=True)]
        images = [urljoin(url, i["src"]) for i in soup.find_all('img', src=True)]
        scripts = [urljoin(url, s["src"]) for s in soup.find_all('script', src=True)]
        title = soup.title.string
        return cls(url=url, title=title, links=links, images=images, scripts=scripts)


async def fetch(url, session):
        async with session.get(url, timeout=5) as response:
            return await response.read()


async def soupify(sem, url, session, depth, max_depth):
    try:
        async with sem:
            page = await fetch(url, session)

        print("{}: {}".format(depth, url))

        wb = WebPage.from_soup(BeautifulSoup(page, "html.parser"), url)
        STORE[url] = wb

        # if we haven't hit max_depth yet work our links to recurse over
        if depth < max_depth:
            valid_targets = set([t for t in wb.links if url in t and t not in STORE])
            tasks = [asyncio.ensure_future(soupify(sem, vt, session, depth+1, max_depth)) for vt in valid_targets]
            return await asyncio.gather(*tasks)

    except (asyncio.TimeoutError, aiohttp.client_exceptions.ServerDisconnectedError, aiohttp.client_exceptions.ClientOSError) as e:
        print(e)
        STORE[url] = WebPage(url=url)


async def start(loop, url, max_depth):
    depth = 1
    sem = asyncio.Semaphore(2)
    async with aiohttp.ClientSession(loop=loop) as session:
        await soupify(sem, url, session, depth, max_depth)


def main():
    url = "https://blog.hartleybrody.com/"
    max_depth = 2
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop, url, max_depth))
    print("LOOP DONE")
    for url, webpage in STORE.items():
        print("{}: {}".format(url, webpage.title))

    # Network PLot

    edges = []
    for url, webpage in STORE.items():
        for link in webpage.links:
            edges.append((url, link))

    print(edges)
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    G.add_edges_from(edges)


if __name__ == "__main__":
    main()
