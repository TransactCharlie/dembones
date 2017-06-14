import aiohttp
from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urljoin, urlparse
import json


STORE = {}


async def fetch(url, session):
        async with session.get(url, timeout=5) as response:
            return await response.read()


async def soupify(sem, url, session, depth, max_depth):

    # WRITE STORE ENTRY STRAIGHT AWAY
    if url not in STORE:
        STORE[url] = None

    if depth >= max_depth:
        return await asyncio.sleep(0)

    print("{}: {}".format(depth, url))
    try:
        async with sem:
            foo = await fetch(url, session)

        b = BeautifulSoup(foo, "html.parser")
        STORE[url] = len(str(b))
        links = b.find_all('a', href=True)
        potential_targets = (urljoin(url, l["href"]) for l in links)
        valid_targets = set([
            t for t in potential_targets
            if urlparse(t).hostname == urlparse(url).hostname
            and t not in STORE
        ])
        tasks = []
        for vt in valid_targets:
            tasks.append(asyncio.ensure_future(soupify(sem, vt, session, depth + 1, max_depth)))

        return await asyncio.gather(*tasks)

    except (asyncio.TimeoutError, aiohttp.client_exceptions.ServerDisconnectedError) as e:
        print(e)
        STORE[url] = -1
        return await asyncio.sleep(0)


async def start(loop, url, max_depth):
    depth = 1
    sem = asyncio.Semaphore(7)
    async with aiohttp.ClientSession(loop=loop) as session:
        await soupify(sem, url, session, depth, max_depth)


def main():
    url = "https://www.bbc.co.uk/"
    max_depth = 5
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop, url, max_depth))
    print("LOOP DONE")
    print(json.dumps(STORE, indent=4))


if __name__ == "__main__":
    main()
