from logging import getLogger
from typing import Union

from disnake import CommandInter, TextChannel, Thread
from disnake.ext.commands import Cog, default_member_permissions, slash_command

from ezar import Ezar
from ezar.backend.config import Colors, Database, Emojis

log = getLogger(__name__)


class GuildLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot
        self.db = Database.guild_logs

    @slash_command()
    @default_member_permissions(manage_guild=True)
    async def logs(self, itr: CommandInter):
        """The logs parent command"""

    @logs.sub_command()
    async def subscribe(self, itr: CommandInter, channel: Union[TextChannel, Thread]):
        """Subscribe to certain logs.

        Parameters
        ----------
        channel: The channel to send the logs to."""
        if not channel.permissions_for(itr.guild.me).send_messages:
            return await itr.response.send_message(f"{Emojis.cross} I require the `send_messages` permission to send messages to {channel.mention}.")


def setup(bot: Ezar):
    bot.add_cog(GuildLogs(bot))
