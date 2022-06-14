from logging import getLogger
from disnake.ext.commands import Cog
from ezar import Ezar

log = getLogger(__name__)


class Listeners(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener("on_ready")
    async def when_connected(self):
        log.info(f"{self.bot.user} is alive")


def setup(bot: Ezar):
    bot.add_cog(Listeners(bot))
