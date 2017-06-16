from dembones.collector import Collector
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("CLI")


def main():
    log.info("Starting")
    c = Collector(max_concurrent_fetches=5)
    c.start_collection("https://blog.hartleybrody.com/")


if __name__ == "__main__":
    main()