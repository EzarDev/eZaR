from platform import python_version
from typing import Optional

from disnake import (
    ApplicationCommandInteraction,
    Object,
    Permissions,
    __version__,
    version_info,
)
from disnake.ext.commands import Cog, Range, slash_command
from disnake.utils import MISSING, format_dt, oauth_url

from ezar import Ezar
from ezar.backend.config import Bot
from ezar.utils.embed import Embeb

CREDITS_DESC = """
**Libraries:**
Disnake - https://disnake.dev | https://discord.gg/disnake
Python - https://python.org

**Frontend** ~~copy~~ **insipiration:**
Monty Python - https://github.com/onerandomusername/monty-python

**Contributors:**
[toolifelesstocode](https://github.com/toolifelesstocode)
[ooliver1](https://github.com/ooliver1)
[shruuub](https://github.com/shruuub)
[EnokiUN](https://github.com/EnokiUN)
"""

STATS_DESC = """
Version: `{bot_version}`
Python Version: `{python_version}`
Disnake Version: `{dis_version} {dis_rl}`
Online since: {bot_uptime}

Servers: `{guild_count}`
Users: `{user_count}`
Channels: `{channel_count}`
"""


class Meta(Cog):
    """Meta commands, or 'bot-related' commands"""

    def __init__(self, bot: Ezar):
        self.bot = bot

    @slash_command()
    async def ezar(self, itr: ApplicationCommandInteraction):
        """`ezar` Parent command"""
        ...

    @ezar.sub_command()
    async def stats(self, itr: ApplicationCommandInteraction):
        """Statistics on the current build."""
        stats_embed = Embeb(
            description=STATS_DESC.format(
                bot_version=Bot.version,
                python_version=python_version(),
                dis_version=__version__,
                dis_rl=version_info.releaselevel,
                bot_uptime=format_dt(self.bot.start_time, style="R"),
                guild_count=len(self.bot.guilds),
                user_count=len(self.bot.users),
                channel_count=len([g.channels for g in self.bot.guilds]),
            )
        )
        stats_embed.set_author(name="Statistics", icon_url=self.bot.user.display_avatar)
        return await itr.response.send_message(embed=stats_embed)

    @ezar.sub_command()
    async def ping(self, itr: ApplicationCommandInteraction):
        """Shows how long the response time is."""
        ping_embed = Embeb(
            title="🏓 Pong!",
            description=f"Bot Latency: {round(self.bot.latency * 1000)}ms",
            success=True,
        )
        return await itr.response.send_message(embed=ping_embed)

    @ezar.sub_command()
    async def support(self, itr: ApplicationCommandInteraction):
        """Get an invite to the support server."""
        return await itr.response.send_message(
            f"Have any issues or queries? Join the support server: https://discord.gg/{Bot.support_inv_url}",
            ephemeral=True,
        )

    @ezar.sub_command()
    async def credits(self, itr: ApplicationCommandInteraction):
        """Everything/person who made eZaR possible."""
        creds_embed = Embeb(title="Credits", description=CREDITS_DESC)
        return await itr.response.send_message(embed=creds_embed)

    @ezar.sub_command()
    async def invite(
        self,
        itr: ApplicationCommandInteraction,
        server_id: Optional[str] = None,
        permissions: Optional[Range[0, Permissions.all().value]] = None,
        hidden: bool = True,
    ):
        """Get a bot invite URL.

        Parameters
        ----------
        server_id: The server ID the invite is directed to.
        permissions: The permissions I should have.
        hidden: Whether the invite URL should be sent publicly or be hidden.
        """
        if permissions is None:
            perms = Bot.invite_perms
        else:
            perms = Permissions(permissions)
            # Useless permissions
            perms.administrator = False
            perms.use_slash_commands = False
            perms.view_guild_insights = False
            perms.mention_everyone = False
            perms.send_tts_messages = False
            perms.start_embedded_activities = False
            perms.stream = False

        inv_url = oauth_url(
            self.bot.user.id,
            permissions=perms,
            guild=Object(server_id) if server_id is not None else MISSING,
        )
        await itr.response.defer(ephemeral=hidden)
        return await itr.edit_original_message(f"Here is your invite URL: {inv_url}")


def setup(bot: Ezar):
    """Loading the Meta cog"""
    bot.add_cog(Meta(bot))
