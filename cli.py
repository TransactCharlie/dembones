from dembones.collector import Collector
import dembones.urlvalidators as uv
import logging
import click


def initialise_logger(level):
    logging.basicConfig(level=level)
    return logging.getLogger("DEMBONES")


def determine_validator(vt):
    if vt == "same-domain":
        return uv.same_domain
    if vt == "same-domain-up-path":
        return uv.same_domain_up_path


@click.group()
def dembones():
    pass


@click.option("-mc,", "--max-concurrency", help="Max fetch tasks at any one time", default=5)
@click.option("-md", "--max-depth", help="Maximum recursion when collecting URLS", default=3)
@click.option("-vt", "--validate-targets", help="How to decide if we should recurse a link",
              type=click.Choice(["same-domain", "same-domain-up-path"]), default="same-domain")
@click.option("-v", "--verbose", help="Enable Verbose Mode", is_flag=True)
@click.argument("url")
def scrape(mc, md, vt, v, url):
    log = initialise_logger(logging.DEBUG if v else logging.INFO)

    validate = determine_validator(vt)

    log.info("Starting Collection")
    c = Collector(max_concurrent_fetches=mc, max_depth=md, target_validator=validate)
    c.start_collection(url)


# Simple helper for invoking in pycharm / ide for debugger
if __name__ == "__main__":
    scrape(5, 3, "same-domain", True, "https://blog.hartleybrody.com/")
