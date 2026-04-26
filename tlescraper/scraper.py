# tlescraper\scraper.py
from urllib.request import urlopen
import ssl
import os
import logging
from tlescraper.utils import retry

logger = logging.getLogger(__name__)

CELESTRAK_BASE_URL = "https://celestrak.com/NORAD/elements"

# celestrak.com のSSL証明書が期限切れになることがある。
# MITM リスクは運用上許容済み。
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE
logger.warning("SSL certificate verification is disabled for celestrak.com (CERT_NONE). MITM risk accepted.")


@retry(max_retry=3, retry_interval=0.1, raise_on=[ValueError])
def get_tle(CATNR: str):
    url = f"{CELESTRAK_BASE_URL}/gp.php?CATNR={CATNR}"
    logger.debug(f"Loading {url}")
    with urlopen(url, context=_ssl_ctx) as response:
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
