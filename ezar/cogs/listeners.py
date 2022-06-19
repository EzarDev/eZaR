from logging import getLogger

from disnake.ext.commands import Cog

from ezar import Ezar

log = getLogger(__name__)


class Listeners(Cog):
    """Listeners ('events') go here"""

    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener("on_ready")
    async def when_connected(self):
        log.info(f"{self.bot.user} is alive")


def setup(bot: Ezar):
    """Loading the Listeners cog"""
    bot.add_cog(Listeners(bot))
