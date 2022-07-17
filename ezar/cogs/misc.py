from typing import Literal, Optional

from disnake import CommandInter, Member, User
from disnake.ext.commands import Cog, slash_command

from ezar import Ezar
from ezar.backend.config import Colors
from ezar.utils.embed import Embeb


class Miscellaneous(Cog):
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
        avatar_embed.set_image(url=itr.guild.icon.with_size(1024).url)
        avatar_embed.set_author(
            name=itr.guild.name,
            icon_url=itr.guild.icon if itr.guild.icon else itr.guild.gen,
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
        info_embed = Embeb(
            description=itr.guild.description,
        )
        info_embed.set_author(name=itr.guild.name, icon_url=itr.guild.icon)
        info_embed.set_thumbnail(url=itr.guild.icon.url if itr.guild.icon else "")
        info_embed.add_field(name="Owner", value=f"`{itr.guild.owner}`")
        await itr.response.send_message(embed=info_embed)


def setup(bot: Ezar):
    bot.add_cog(Miscellaneous(bot))
