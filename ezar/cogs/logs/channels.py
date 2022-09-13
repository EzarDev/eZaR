from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from disnake.abc import GuildChannel
from disnake.ext.commands import Cog

from ezar.cogs.logs import (
    ENUM_HANDLER,
    INDEX_HANDLER,
    NAMED_SNOWFLAKE_HANDLER,
    PLAIN_HANDLER,
    UNIT_HANDLER,
    parse_update,
    query_config,
)
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from ezar import Ezar

UPDATE_HANDLERS: dict[str, Callable[[Any], str]] = {
    "bitrate": lambda b: f"`{b // 1000}kbps`",
    "category": NAMED_SNOWFLAKE_HANDLER,
    "default_auto_archive_duration": UNIT_HANDLER("m"),
    "name": PLAIN_HANDLER,
    "nsfw": PLAIN_HANDLER,
    "overwrites": lambda o: ", ".join(f"`{t.name}`" for t in sorted(o.keys())),
    "permissions_synced": PLAIN_HANDLER,
    "position": INDEX_HANDLER,
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
            changes = parse_update(handlers=UPDATE_HANDLERS, before=before, after=after)

            if changes:
                embed = Embeb(
                    title="Channel Edited",
                    description=CHANNEL_EDITED.format(channel=after, changed=changes),
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
