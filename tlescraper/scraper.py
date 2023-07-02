# tlescraper\scraper.py
from urllib.request import urlopen
import os
import logging
from tlescraper.utils import retry

logger = logging.getLogger(__name__)

CERESTRACK_BASE_URL = "https://celestrak.com/NORAD/elements/"


@retry(max_retry=3, retry_interval=0.1, raise_on=[ValueError])
def get_tle(CATNR: str):
    url = f"{CERESTRACK_BASE_URL}/gp.php?CATNR={CATNR}"
    # Get TLE from URL
    logger.debug(f"Loading {url}")
    response = urlopen(url)

    content = response.read().decode("utf-8")
    content = "\n".join(content.splitlines()) + "\n"
    if len(content.splitlines()) != 3:
        raise ValueError(f"Error loading {url}: {content}")
    return content


def save_tle(CATNR: str, output_dir) -> str:
    """Saves the TLE of a satellite to a file"""
    filename = os.path.join(output_dir, f"{CATNR}.txt")

    content = get_tle(CATNR)
    logger.debug(f"Content: {content}")

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w", encoding="ascii") as f:
        f.write(content)
    return content
