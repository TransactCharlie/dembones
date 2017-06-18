from dembones.collector import Collector
import logging
import click


def initialise_logger(level):
    logging.basicConfig(level=level)
    return logging.getLogger("DEMBONES")


@click.group()
def dembones():
    pass


@click.option("-mc,", "--max-concurrency", help="Max fetch tasks at any one time", default=5)
@click.option("-md", "--max-depth", help="Maximum recursion when collecting URLS", default=3)
@click.option("-v", "--verbose", help="Enable Verbose Mode", is_flag=True)
@click.argument("url")
def scrape(mc, md, v, url):
    log = initialise_logger(logging.DEBUG if v else logging.INFO)

    log.info("Starting Collection")
    c = Collector(max_concurrent_fetches=mc, max_depth=md)
    c.start_collection(url)


# Simple helper for invoking in pycharm / ide for debugger
if __name__ == "__main__":
    scrape(5, 3, True, "https://blog.hartleybrody.com/")
