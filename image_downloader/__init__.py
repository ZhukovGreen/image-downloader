import logging
import pathlib
import sys

import aiofiles
import aiohttp
import click
import yarl
from envparse import env

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG if env.bool("DEBUG", default=False) else logging.INFO,
    format=">> %(message)s",
)

logger = logging.getLogger(__name__)


async def app(src: pathlib.Path, target: pathlib.Path):
    """Download images from src file urls to the target."""
    if not target.is_dir():
        raise click.BadParameter(
            f"Target should be a directory. Got {repr(target)}"
        )
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(src) as f:
            async for line in f:
                logger.info(f"Received {repr(line).strip()} for processing")
                img_name = yarl.URL(line).name.strip()
                try:
                    async with session.get(line.strip()) as r:
                        if r.status == 200:
                            logger.info(
                                f"File {repr(img_name)}"
                                f" downloaded successfully."
                            )
                            async with aiofiles.open(
                                target / img_name, mode="wb"
                            ) as image_file:
                                await image_file.write(await r.read())
                except (aiohttp.InvalidURL, aiohttp.ClientConnectionError):
                    # if url is bad, we skip it, but continue
                    logger.error(
                        f"URL {repr(line.strip())} is not valid. Skipping..."
                    )
