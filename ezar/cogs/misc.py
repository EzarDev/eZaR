from inspect import cleandoc
from typing import Literal, Optional

from disnake import CommandInter, Member, User, utils
from disnake.ext.commands import Cog, slash_command

from ezar import Ezar
from ezar.backend.config import Colors
from ezar.utils.embed import Embeb


class Miscellaneous(Cog, slash_command_attrs={"dm_permissions": False}):
    """Miscellaneous/not-important commands"""

    def __init__(self, bot: Ezar):
        self.bot = bot

    @slash_command()
    async def icon(self, itr: CommandInter):
        """Icon/Profile-Picture-related commands"""

    @icon.sub_command("server")
    async def icon_server(self, itr: CommandInter):
        """Returns the server icon URL."""
        avatar_embed = Embeb()
        avatar_embed.set_image(
            url=itr.guild.icon.with_size(1024).url if itr.guild.icon else None
        )
        # TODO: generate an image instead of returning None
        avatar_embed.set_author(
            name=itr.guild.name,
            icon_url=itr.guild.icon if itr.guild.icon else None,
        )
        await itr.response.send_message(embed=avatar_embed)

    @icon.sub_command("user")
    async def icon_user(
        self,
        itr: CommandInter,
        user: Optional[User] = None,
        type: Literal["global", "local"] = "local",
    ):
        """Returns a user's avatar.

        Parameters
        ----------
        user: The user to get the avatar of.
        type: The type of avatar to get."""
        if user is None:
            user: Member = itr.user

        avatar_embed = Embeb(
            color=user.color if user in itr.guild.members else Colors.purple
        )
        if type == "global":
            avatar_embed.set_image(url=user.avatar.url or user.default_avatar.url)
            avatar_embed.set_author(
                name=user.name, icon_url=user.avatar.url or user.default_avatar.url
            )
        elif type == "local":
            avatar_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            avatar_embed.set_image(url=user.display_avatar.url)

        return await itr.send(embed=avatar_embed)

    @slash_command()
    async def info(self, itr: CommandInter):
        """Information-related commands"""

    @info.sub_command("server")
    async def info_server(self, itr: CommandInter):
        """Returns the server information."""
        guild = itr.guild
        members = cleandoc(
            f"""
        Humans: `{len([m for m in guild.members if not m.bot])}`
        Bots: `{len([m for m in guild.members if m.bot])}`
        """
        )
        channels = cleandoc(
            f"""
        Text: `{len(guild.text_channels)}`
        Voice: `{len(guild.voice_channels)}`
        Stages: `{len(guild.stage_channels)}`
        Forums: `{len(guild.forum_channels)}`
        """
        )
        if len(guild.roles) > 25:
            roles = "Too many roles to display."
        else:
            roles = ", ".join(
                sorted(
                    [r.mention for r in guild.roles if r.id != guild.id],
                    key=lambda r: r.position,
                )
            )
        vanity = await guild.vanity_invite(use_cached=True)
        info_embed = Embeb(
            description=guild.description,
        )
        info_embed.set_author(name=guild.name, icon_url=guild.icon)
        info_embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        info_embed.set_image(
            url=guild.banner.url
            if guild.banner
            else guild.splash.url
            if guild.splash
            else ""
        )
        info_embed.add_field(name="Owner", value=guild.owner)
        info_embed.add_field(name="ID", value=guild.id)
        info_embed.add_field(name=f"Members [{len(guild.members)}]", value=members)
        info_embed.add_field(name="Created", value=utils.format_dt(guild.created_at)),
        info_embed.add_field(
            name="Rule Channel",
            value=guild.rules_channel.mention
            if guild.rules.channel
            else "No rules channel",
        )
        info_embed.add_field(
            name="Vanity URL",
            value=f"[{guild.vanity_url_code}]({vanity.url if vanity else ''})",
        )
        info_embed.add_field(
            name=f"Channels [{len(guild.channels)}]", value=channels, inline=False
        )
        info_embed.add_field(
            name=f"Roles [{len(guild.roles)}]", value=roles, inline=False
        )
        await itr.response.send_message(embed=info_embed)


def setup(bot: Ezar):
    bot.add_cog(Miscellaneous(bot))
