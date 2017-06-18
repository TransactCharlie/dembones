import aiohttp
from bs4 import BeautifulSoup
import asyncio
from dembones.webpage import WebPage
import dembones.urlvalidators as uv

import logging
log = logging.getLogger(__name__)


class Collector:

    url_hash = {}

    def __init__(self, max_concurrent_fetches=3, max_depth=3, fetch_timeout=5,
                 target_validator=uv.same_domain_up_path):
        self.semaphore = asyncio.Semaphore(max_concurrent_fetches)
        self.fetch_timeout = fetch_timeout
        self.max_depth = max_depth
        self.validate_targets = target_validator

    async def fetch(self, url, session):
        """Fetch url using session."""
        async with session.get(url, timeout=self.fetch_timeout) as r:
            return await r.read()

    async def recurse_collect(self, url, session, depth):
        """Fetch url and Soup it. Then work out which links we need to recurse."""

        # Because we are scheduled at the mercy of the reactor loop. It's possible that
        # Some other task is already fetching this page is awaiting the result. Lets check!
        if url in self.url_hash:
            return

        # OK we are the only active task on this reactor. Before we await the page
        # let other potential tasks know that we are working on it.
        self.url_hash[url] = None

        try:
            async with self.semaphore:
                page = await self.fetch(url, session)

            log.debug("Depth {}: Url {}".format(depth, url))

            wp = WebPage.from_soup(BeautifulSoup(page, "html.parser"), url)
            self.url_hash[url] = wp

            # if we haven't hit max_depth yet work out links to recurse over
            if depth < self.max_depth:
                valid_targets = set([
                    t for t in wp.links
                    if t not in self.url_hash
                    and self.validate_targets(url, t)
                ])
                tasks = [self.recurse_collect(vt, session, depth+1) for vt in valid_targets]
                return await asyncio.gather(*tasks)

        # There are a myriad of IO based exceptions that can happen - I don't know all of them.
        # We want to continue processing other tasks though.
        except Exception as e:
            log.error(e)
            # Upgrade our sentinel entry in the hashmap to at least be the WebPage object
            self.url_hash[url] = WebPage(url=url)

    async def start_recursive_collect(self, url, loop):
        """Start our collection using the event loop (loop)"""
        depth = 1
        async with aiohttp.ClientSession(loop=loop) as session:
            await self.recurse_collect(url, session, depth)

    def start_collection(self, url):
        loop = asyncio.get_event_loop()
        log.debug("Collector Event Loop Start")
        loop.run_until_complete(self.start_recursive_collect(url, loop))
        log.debug("Collector Event Loop Exit")
        return {url: wp.to_dict() for url, wp in self.url_hash.items()}
