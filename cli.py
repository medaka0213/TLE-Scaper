import click
import logging
import os
import tlescraper.scraper as ts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cli = click.Group()

TLE_LIST = os.environ.get("TLE_LIST", ["25544", "25399", "25994"])


@cli.command()
@click.argument("CATNR")
def save(catnr):
    """Saves the TLE of a satellite to a file"""
    res = ts.save_tle(catnr)
    click.echo(res)


@cli.command()
@click.argument("catnr-list", nargs=-1)
def save_batch(catnr_list):
    """Saves multiple TLE of a satellite to a file"""
    catnr_list = catnr_list or TLE_LIST
    for catnr in catnr_list:
        res = ts.save_tle(catnr)
        click.echo(res)


if __name__ == "__main__":
    cli()
