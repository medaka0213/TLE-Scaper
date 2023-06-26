import urllib.request
import os
import logging

logger = logging.getLogger(__name__)

CERESTRACK_BASE_URL = "https://celestrak.com/NORAD/elements/"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")


def _save_url_to_file(url: str, filename: str, encoding: str = "ascii"):
    """Saves the content of a URL to a file"""
    logger.debug(f"Loading {url} to {filename}")
    response = urllib.request.urlopen(url)
    content = response.read().decode("utf-8")
    logger.debug(f"Content: {content}")

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w", encoding=encoding) as f:
        f.write(content.replace("\r", ""))
    return content


def save_tle(CATNR: str):
    """Saves the TLE of a satellite to a file"""
    url = f"{CERESTRACK_BASE_URL}/gp.php?CATNR={CATNR}"
    path = os.path.join(OUTPUT_DIR, f"{CATNR}.txt")

    logger.info(f"Saving TLE of {CATNR} to {path}")
    return _save_url_to_file(url, path)
