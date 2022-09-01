from asyncio import run
from logging import INFO, basicConfig, getLogger
from pathlib import Path

from disnake.ext.commands import ExtensionError

from ezar.backend.config import Config
from ezar.utils.ezar import Ezar


async def setup() -> None:
    """Starts up the entire instance."""
    bot = Ezar()
    log = getLogger(__name__)
    basicConfig(
        format="[%(asctime)s] | %(name)s | %(levelname)s | %(message)s",
        level=INFO,
        datefmt="%Y-%m-%d - %H:%M:%S",
    )

    for c in Path("ezar/cogs").glob("**/*.py"):
        if c.suffix == ".py":
            try:
                ext = ".".join(c.parts)[:-3]
                bot.load_extension(ext)
                log.info("%s has loaded.", ext)
            except ExtensionError as err:
                log.error("{n}: {e}".format(n=err.name, e=err))
                log.info("Aborting connection.")
                exit(0)
    bot.load_extension("jishaku")

    await bot.start(Config.main_token if not bot.beta else Config.beta_token)
    return


if __name__ == "__main__":
    run(setup())
