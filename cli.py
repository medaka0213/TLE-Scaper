import click
import logging
import tlescraper.scraper as ts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cli = click.Group()


@cli.command()
@click.argument("CATNR")
def save(catnr):
    """Saves the TLE of a satellite to a file"""
    res = ts.save_tle(catnr)
    click.echo(res)


if __name__ == "__main__":
    cli()
