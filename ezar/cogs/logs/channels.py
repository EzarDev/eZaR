from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from disnake.abc import GuildChannel
from disnake.ext.commands import Cog

from ezar.cogs.logs import query_config
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from enum import Enum

    from ezar import Ezar

PLAIN_HANDLER: Callable[[Any], str] = lambda p: f"`{p}`"
ENUM_HANDLER: Callable[[Enum], str] = lambda e: f"`{e.name.replace('_', ' ').title()}`"
UNIT_HANDLER: Callable[[str], Callable[[int], str]] = lambda u: lambda s: f"`{s}{u}`"
TO_CHECK: dict[str, Callable[[Any], str]] = {
    "bitrate": UNIT_HANDLER("bps"),
    "category": lambda c: f"`{c.name}` (`{c.id}`)",
    "default_auto_archive_duration": UNIT_HANDLER("m"),
    "name": PLAIN_HANDLER,
    "nsfw": PLAIN_HANDLER,
    "overwrites": lambda o: ", ".join(f"`{t.name}`" for t in sorted(o.keys())),
    "permissions_synced": PLAIN_HANDLER,
    "position": lambda p: f"`{p + 1}`",
    "rtc_region": PLAIN_HANDLER,
    "slowmode_delay": UNIT_HANDLER("s"),
    "topic": PLAIN_HANDLER,
    "type": ENUM_HANDLER,
    "user_limit": PLAIN_HANDLER,
    "video_quality_mode": ENUM_HANDLER,
}
CHANNEL_EDITED = """

{channel.mention} (`{channel.name}` - `{channel.id}`) was edited.

**Changes**:
{changed}

""".strip()


class ChannelLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener()
    async def on_guild_channel_create(self, channel: GuildChannel):
        guild = channel.guild

        if log_channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_channel_create"
        ):
            category_text = (
                (
                    "in the category "
                    f"`{channel.category.name}` (`{channel.category.id}`) "
                    + ("with" if channel.permissions_synced else "without")
                    + " permissions synced"
                )
                if channel.category
                else "without a category"
            )
            description = (
                f"{channel.mention} (`{channel.id}` - `{channel.name}`) was created "
                + category_text
            )

            embed = Embeb(
                title="Channel Created", description=description, success=True
            )

            await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_update(self, before: GuildChannel, after: GuildChannel):
        guild = after.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_channel_update"
        ):
            changes: list[str] = []

            # Go through all checkable, make sure the human readables are not equal.
            # Except to handle if that attribute is not on this type.
            for attribute, modifier in sorted(TO_CHECK.items()):
                try:
                    before_change = modifier(getattr(before, attribute))
                    after_change = modifier(getattr(after, attribute))
                except AttributeError:
                    continue
                else:
                    if before_change != after_change:
                        changes.append(
                            f"`{attribute}` - {before_change} -> {after_change}"
                        )

            if changes:
                changed = "\n".join(changes)
                embed = Embeb(
                    title="Channel Edited",
                    description=CHANNEL_EDITED.format(channel=after, changed=changed),
                )
                await channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel: GuildChannel):
        guild = channel.guild

        if log_channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_channel_delete"
        ):
            description = f"`{channel.name}` (`{channel.id}`)"
            embed = Embeb(
                title="Channel Deleted", description=description, failure=True
            )
            await log_channel.send(embed=embed)


def setup(bot: Ezar):
    bot.add_cog(ChannelLogs(bot))
