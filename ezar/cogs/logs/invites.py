from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from disnake.ext.commands import Cog
from disnake.utils import format_dt

from ezar.cogs.logs import query_config
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from disnake import Invite

    from ezar import Ezar


log = getLogger(__name__)


class InviteLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener()
    async def on_invite_create(self, invite: Invite):
        guild = invite.guild

        if guild is None:
            return

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="invite_create"
        ):
            description = self.format_invite(invite, fmt="created in")

            embed = Embeb(title="Invite Created", description=description, success=True)
            await channel.send(embed=embed)

    @Cog.listener()
    async def on_invite_delete(self, invite: Invite):
        guild = invite.guild

        if guild is None:
            return

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="invite_delete"
        ):
            description = self.format_invite(invite, fmt="deleted for")

            embed = Embeb(title="Invite Deleted", description=description, failure=True)
            await channel.send(embed=embed)

    @staticmethod
    def format_invite(invite: Invite, fmt: str) -> str:
        invite_ch = invite.channel

        if hasattr(invite_ch, "mention"):
            channel_fmt = (
                f"{invite_ch.mention} (`{invite_ch.name}`"  # type: ignore
                f" - `{invite_ch.id}`)"  # type: ignore
            )
        elif hasattr(invite_ch, "name"):
            channel_fmt = f"{invite_ch.name} (`{invite_ch.id}`)"  # type: ignore
        elif invite_ch is not None:
            channel_fmt = f"`{invite_ch.id}`"
        else:
            channel_fmt = "no channel?"

        description = f"`{invite.code}` was {fmt} {channel_fmt}"

        if invite.inviter:
            description += (
                f" by {invite.inviter.mention} (`{invite.inviter.name}` "
                f"- `{invite.inviter.id}`)"
            )

        if invite.target_application:
            description += f" for the application `{invite.target_application.name}`"

        if invite.guild_scheduled_event:
            description += (
                f" for the scheduled event `{invite.guild_scheduled_event.name}`"
                f" (`{invite.guild_scheduled_event.id}`)"
            )

        if invite.expires_at:
            description += f" which expires at {format_dt(invite.expires_at)}"

        return description


def setup(bot: Ezar):
    bot.add_cog(InviteLogs(bot))
