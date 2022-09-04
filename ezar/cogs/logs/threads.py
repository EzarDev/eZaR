from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from disnake.ext.commands import Cog

from ezar.cogs.logs import (
    ENUM_HANDLER,
    PLAIN_HANDLER,
    UNIT_HANDLER,
    parse_update,
    query_config,
)
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from disnake import Thread

    from ezar import Ezar


UPDATE_HANDLERS: dict[str, Callable[[Any], str]] = {
    "auto_archive_duration": UNIT_HANDLER("m"),
    "archived": PLAIN_HANDLER,
    "invitable": PLAIN_HANDLER,
    "locked": PLAIN_HANDLER,
    "name": PLAIN_HANDLER,
    "slowmode_delay": UNIT_HANDLER("s"),
    "type": ENUM_HANDLER,
}
THREAD_EDITED = """

{thread.mention} (`{thread.name}` - `{thread.id}`) was edited.

**Changes**:
{changed}

""".strip()


class ThreadLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener()
    async def on_thread_create(self, thread: Thread):
        guild = thread.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="thread_create"
        ):
            description = (
                f"{thread.mention} (`{thread.name}` - `{thread.id}`) was created "
                f"(`{thread.type.name.replace('_', ' ').title()}`) under the channel "
                f"{thread.parent.mention} "  # type: ignore
                f"(`{thread.parent.name}` - `{thread.parent.id}`)."  # type: ignore
            )
            embed = Embeb(title="Thread Created", description=description, success=True)
            await channel.send(embed=embed)

    @Cog.listener()
    async def on_thread_update(self, before: Thread, after: Thread):
        guild = after.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="thread_update"
        ):
            changes = parse_update(handlers=UPDATE_HANDLERS, before=before, after=after)

            if changes:
                embed = Embeb(
                    title="Thread Edited",
                    description=THREAD_EDITED.format(thread=after, changed=changes),
                )
                await channel.send(embed=embed)

    @Cog.listener()
    async def on_thread_delete(self, thread: Thread):
        guild = thread.guild

        if log_channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="thread_delete"
        ):
            description = f"`{thread.name}` (`{thread.id}`)"
            embed = Embeb(title="Thread Deleted", description=description, failure=True)
            await log_channel.send(embed=embed)


def setup(bot: Ezar):
    bot.add_cog(ThreadLogs(bot))
