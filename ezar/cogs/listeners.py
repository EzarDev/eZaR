from logging import getLogger
from typing import Union

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Cog, Context, NotOwner

from ezar import Ezar
from ezar.backend.config import Bot
from ezar.utils.embed import Embeb

log = getLogger(__name__)


error_description = """
An error occurred while executing this command.
If you do not understand this error or think it is an internal error,
please report it in our [support server](discord.gg/{invite}).

```py
{exc}
```
"""


class Listeners(Cog):
    """Listeners ('events') go here"""

    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener("on_ready")
    async def when_connected(self):
        log.info(f"{self.bot.user} is alive")

    @Cog.listener("on_slash_command_error")
    @Cog.listener("on_command_error")
    async def command_error(
        self, itr: Union[ApplicationCommandInteraction, Context], exc: Exception
    ):
        if isinstance(exc, NotOwner):
            return

        desc = error_description.format(invite=Bot.support_inv_url, exc=exc)
        error_embed = Embeb(description=desc, failure=True)

        if isinstance(itr, Context):
            command_name = itr.command.qualified_name if itr.command else "None"
            log.error(f"Error with command {command_name}: {exc}")
            return await itr.reply(embed=error_embed)
        else:
            command_name = itr.application_command.qualified_name
            log.error(f"Error with slash command {command_name}: {exc}")
            return await itr.send(embed=error_embed)


def setup(bot: Ezar):
    """Loading the Listeners cog"""
    bot.add_cog(Listeners(bot))
