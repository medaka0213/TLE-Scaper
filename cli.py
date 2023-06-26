import click
import logging
import os
import tlescraper.scraper as ts
import tlescraper.htmlrender as hr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cli = click.Group()

TLE_LIST = os.environ.get("TLE_LIST", "25544, 48274, 20580")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")


@cli.command()
@click.argument("CATNR")
def save(catnr):
    """Saves the TLE of a satellite to a file"""
    res = ts.save_tle(catnr, OUTPUT_DIR)
    click.echo(res)


@cli.command()
@click.argument("catnr-list", nargs=-1)
def save_batch(catnr_list):
    """Saves multiple TLE of a satellite to a file"""
    _tle_list = [x.strip() for x in TLE_LIST.split(",")]
    catnr_list = catnr_list or _tle_list
    for catnr in catnr_list:
        res = ts.save_tle(catnr, OUTPUT_DIR)
        click.echo(res)


@cli.command()
@click.argument("output-dir", default=OUTPUT_DIR)
def gen_html(output_dir):
    """Generates an index.html file for a directory"""
    hr.generate_index_html(output_dir)


if __name__ == "__main__":
    cli()
