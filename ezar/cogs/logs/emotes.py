from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from disnake.ext.commands import Cog

from ezar.cogs.logs import query_config
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from disnake import Emoji, Guild, GuildSticker

    from ezar import Ezar


log = getLogger(__name__)
STICKER_DESC = """

`{sticker.name}` (:{sticker.emoji}: - `{sticker.id}`)
```
{sticker.description}
```

""".strip()


class EmoteLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener()
    async def on_guild_emojis_update(
        self, guild: Guild, before: tuple[Emoji, ...], after: tuple[Emoji, ...]
    ):
        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_emojis_update"
        ):
            diff = (set(after) ^ set(before)).pop()

            if len(before) < len(after):
                description = f"{diff} (`{diff.name}` - `{diff.id}`)."
                embed = Embeb(
                    title="Emoji Created", description=description, success=True
                )
            else:
                description = f"`{diff.name}` (`{diff.id}`)"
                embed = Embeb(
                    title="Emoji Deleted", description=description, failure=True
                )

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_stickers_update(
        self,
        guild: Guild,
        before: tuple[GuildSticker, ...],
        after: tuple[GuildSticker, ...],
    ):
        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_stickers_update"
        ):
            diff = (set(after) ^ set(before)).pop()

            description = STICKER_DESC.format(sticker=diff)

            if len(before) < len(after):
                embed = Embeb(
                    title="Sticker Created", description=description, success=True
                )
            else:
                embed = Embeb(
                    title="Sticker Deleted", description=description, failure=True
                )

            await channel.send(embed=embed)


def setup(bot: Ezar):
    bot.add_cog(EmoteLogs(bot))
