from logging import getLogger

from disnake import CommandInter, Guild
from disnake.ext.commands import (
    Cog,
    CommandError,
    Context,
    MissingPermissions,
    NotOwner,
)

from ezar import Ezar
from ezar.backend.config import Bot, Config
from ezar.utils.embed import Embeb

log = getLogger(__name__)


class Listeners(Cog):
    """Listeners ('events') go here"""

    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener("on_ready")
    async def when_connected(self):
        log.info("{0} is has awoken ({1})".format(str(self.bot.user), self.bot.user.id))

    @Cog.listener("on_guild_join")
    async def guild_add(self, guild: Guild):
        self.post_channel = await self.bot.getch_channel(Config.blist_log_channel_id)
        guild_add_embed = (
            Embeb(
                success=True,
            )
            .set_footer(
                text="Created on {0}".format(
                    guild.created_at.strftime("%d-%m-%Y %H:%M")
                )
            )
            .set_author(
                name="Guild Add: {0}".format(guild.name),
                icon_url=guild.icon.url if guild.icon else "",
            )
            .set_thumbnail(url=guild.icon.url if guild.icon else "")
            .add_field(
                name="Owner",
                value="{0} {1}".format(str(guild.owner), str(guild.owner.id)),
            )
            .add_field(name="ID", value=guild.id)
            .add_field(
                name="Members",
                value="Total: `{0}`\nHumans: `{1}`\nBots: `{2}`".format(
                    guild.member_count,
                    len([m for m in guild.members if not m.bot]),
                    len([m for m in guild.members if m.bot]),
                ),
            )
            .add_field(name="New Guild Count", value=len(self.bot.guilds))
        )
        log.info("Guild Add: {0}, {1}".format(guild.name, guild.id))
        return await self.post_channel.send(embed=guild_add_embed)

    @Cog.listener("on_guild_remove")
    async def guild_remove(self, guild: Guild):
        guild_rem_embed = (
            Embeb(
                failure=True,
            )
            .set_footer(
                text="Created on {0}".format(
                    guild.created_at.strftime("%d-%m-%Y %H:%M")
                )
            )
            .set_author(
                name="Guild Remove: {0}".format(guild.name),
                icon_url=guild.icon.url if guild.icon else "",
            )
            .set_thumbnail(url=guild.icon.url if guild.icon else "")
            .add_field(
                name="Owner",
                value="{0} {1}".format(str(guild.owner), str(guild.owner.id)),
            )
            .add_field(name="ID", value=guild.id)
            .add_field(
                name="Members",
                value="Total: `{0}`\nHumans: `{1}`\nBots: `{2}`".format(
                    guild.member_count,
                    len([m for m in guild.members if not m.bot]),
                    len([m for m in guild.members if m.bot]),
                ),
            )
            .add_field(name="New Guild Count", value=len(self.bot.guilds))
        )
        log.info("Guild Remove: {0}, {1}".format(guild.name, guild.id))
        return await self.post_channel.send(embed=guild_rem_embed)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, exception: CommandError):
        if isinstance(exception, NotOwner):
            return
        else:
            log.critical(
                "Error while executing {0}: {1}".format(
                    ctx.command.qualified_name, exception
                )
            )
            return await ctx.send(
                f"There was an issue executing this command: ```py\n{exception}\n```"
            )

    @Cog.listener()
    async def on_slash_command_error(self, itr: CommandInter, exc: CommandError):
        if isinstance(exc, MissingPermissions):
            no_perms_embed = Embeb(
                failure=True,
                description="You require the {0} permission to run this command.".format(
                    exc.missing_permissions
                ),
            )
            await itr.response.send_message(embed=no_perms_embed)
        else:
            desc = (
                "An error occurred while executing this command. ",
                "If you believe this is a bug or do not understand this error, ",
                "please report it in my [support server](https://discord.gg/{0}).",
                "\n\n```py\n{1}\n```",
            )
            slash_error_embed = Embeb(
                failure=True,
                description=desc.format(
                    Bot.support_inv_url, exc
                ),
            )
            await itr.send(embed=slash_error_embed, ephemeral=True)


def setup(bot: Ezar):
    """Loading the Listeners cog"""
    bot.add_cog(Listeners(bot))
