from os import listdir
from disnake.ext.commands import ExtensionError
from ezar.backend.config.constants import Config
from ezar.utils.ezar import Ezar
from logging import INFO, getLogger, basicConfig


bot = Ezar()
log = getLogger(__name__)
basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=INFO,
    datefmt="%Y-%m-%d - %H:%M:%S",
)


def setup():
    for c_name in listdir("ezar/cogs"):
        if c_name.endswith(".py") and not c_name.startswith("_"):
            try:
                bot.load_extension("ezar.cogs.{c}".format(c=c_name[:-3]))
                bot.load_extension("jishaku")
                log.info("{c} has loaded.".format(c=c_name))
            except ExtensionError as err:
                log.error("{n}: {e}".format(n=err.name, e=err))
                log.info("Aborting connection.")
                exit(0)

    bot.run(Config.main_token if not bot.beta else Config.beta_token)


if __name__ == "__main__":
    setup()
