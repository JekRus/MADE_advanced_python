import argparse
import logging
from lrucache import LRUCache


logging.basicConfig(
    level=logging.INFO,
)


def get_configured_logger(stdout=False, fname='cache.log'):
    logger = logging.getLogger('LRUCache')
    logger.propagate = False

    if stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARNING)
        stream_format = '%(asctime)s %(levelname)-8s %(message)s'
        stream_formatter = logging.Formatter(stream_format)
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(fname)
    file_handler.setLevel(logging.INFO)
    file_format = (
        '%(name)-8s [LINE:%(lineno)-4s]'
        '%(levelname)-8s[%(asctime)s] %(message).100s'
    )
    file_formatter = logging.Formatter(file_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='LRUCache')
    parser.add_argument(
        '-s',
        '--stdout',
        action="store_true",
        help="verbose output"
    )
    args = parser.parse_args()

    logger = get_configured_logger(args.stdout)

    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.get("k3")
    cache.get("k2")
    cache.get("k1")
    cache.set("k3", "val3")
    cache.get("k3")
    cache.get("k2")
    cache.get("k1")
