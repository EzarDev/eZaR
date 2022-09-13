from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from disnake.ext.commands import Cog
from disnake.utils import format_dt

from ezar.cogs.logs import query_config
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from disnake import Member

    from ezar import Ezar


log = getLogger(__name__)


class MemberLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        guild = member.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="member_join"
        ):
            description = (
                f"{member.mention} (`{member}` - `{member.id}`) joined the server. "
                f"Their account was created {format_dt(member.created_at, 'R')}."
            )
            embed = Embeb(title="Member Joined", description=description, success=True)
            await channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        guild = member.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="member_remove"
        ):
            description = (
                f"{member.mention} (`{member}` - `{member.id}`) left the server."
            )

            if member.joined_at:
                description += f" They joined {format_dt(member.joined_at, 'R')}."

            embed = Embeb(title="Member Left", description=description, failure=True)
            await channel.send(embed=embed)


def setup(bot: Ezar):
    bot.add_cog(MemberLogs(bot))
