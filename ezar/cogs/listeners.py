from logging import getLogger

from disnake import CommandInter
from disnake.ext.commands import Cog, Context, NotOwner

from ezar import Ezar
from ezar.backend.config import Bot
from ezar.utils.embed import Embeb

log = getLogger(__name__)


class Listeners(Cog):
    """Listeners ('events') go here"""

    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener("on_ready")
    async def when_connected(self):
        log.info(f"{self.bot.user} is alive")

    @Cog.listener("on_slash_command_error")
    @Cog.listener("on_command_error")
    async def command_error(self, itr: CommandInter, exc: Exception):
        if isinstance(exc, NotOwner):
            return

        desc = (
            "An error occurred while executing this command. ",
            "If you do not understand this error or think it is an internal error, ",
            f"please report it in our [support server](discord.gg/{Bot.support_inv_url}).\n\n",
            f"```py\n{exc}\n```",
        )
        error_embed = Embeb(description=desc, failure=True)

        if isinstance(itr, Context):
            log.error(f"Error with command {itr.command.qualified_name}: {exc}")
            return await itr.reply(embed=error_embed)
        else:
            log.error(f"Error with slash command {itr.command.qualified_name}: {exc}")
            return await itr.send(embed=error_embed)


def setup(bot: Ezar):
    """Loading the Listeners cog"""
    bot.add_cog(Listeners(bot))
