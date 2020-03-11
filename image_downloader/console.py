import asyncio
import logging
import pathlib

import click

from image_downloader import app


@click.command()
@click.option("-v", "--verbose", count=True, help="Verbosity of the tool")
@click.argument("src", type=click.Path(exists=True))
@click.argument("target", type=click.Path(exists=True))
def main(verbose, src, target):
    """Tool which downloads all images and store them in a given dir.

    As input expected a plain-text file, where each line has a URL with the
    image.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    asyncio.run(app(src=pathlib.Path(src), target=pathlib.Path(target),))
