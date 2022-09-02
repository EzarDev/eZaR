from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import DMChannel, Message
from disnake.ext.commands import Cog

from ezar.cogs.logs import query_config
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from ezar import Ezar


class MessageLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if not after.guild:
            return

        if channel := await query_config(
            bot=self.bot, guild_id=after.guild.id, event="message_edit"
        ):
            assert not isinstance(after.channel, DMChannel)
            description = (
                f"`{after.author}` (`{after.author.display_name}`) "
                f"edited a message in {after.channel.mention} "
                f"(`{after.channel.id}` - `{after.channel.name}`)\n"
            )

            truncated_before = (
                before.content[:2000] + "..."
                if len(before.content) > 2003
                else before.content
            ) or "No Content"
            truncated_after = (
                after.content[:2000] + "..."
                if len(after.content) > 2003
                else after.content
            ) or "No Content"

            description += f"**Before**\n```\n{truncated_before}\n```\n"
            description += f"**After**\n```\n{truncated_after}\n```"

            embed = Embeb(title="Message Edited", description=description)

            author = after.author
            username = str(author)
            user_avatar = author.display_avatar

            embed.set_author(name=username, icon_url=user_avatar)

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if not message.guild:
            return

        if channel := await query_config(
            bot=self.bot, guild_id=message.guild.id, event="message_delete"
        ):
            assert not isinstance(message.channel, DMChannel)
            description = (
                f"`{message.author}` (`{message.author.display_name}`) "
                f"deleted a message in {message.channel.mention} "
                f"(`{message.channel.id}` - `{message.channel.name}`)\n"
            )

            truncated_content = (
                message.content[:2000] + "..."
                if len(message.content) > 2003
                else message.content
            ) or "No Content"

            description += f"```\n{truncated_content}\n```"

            embed = Embeb(
                title="Message Deleted", description=description, failure=True
            )

            author = message.author
            username = str(author)
            user_avatar = author.display_avatar

            embed.set_author(name=username, icon_url=user_avatar)

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_bulk_message_delete(self, messages: list[Message]):
        first_message = messages[0]
        if not first_message.guild:
            return

        if channel := await query_config(
            bot=self.bot, guild_id=first_message.guild.id, event="message_delete"
        ):
            assert not isinstance(first_message.channel, DMChannel)
            unique_users = ", ".join(
                f"`{user}`" for user in set(str(m.author) for m in messages)
            )
            description = (
                f"{len(messages)} messages in {first_message.channel.mention} "
                f"(`{first_message.channel.id}` - `{first_message.channel.name}`) by"
                f"{unique_users} were deleted"
            )

            embed = Embeb(title="Multiple Messages Deleted", description=description)

            author = first_message.author
            username = str(author)
            user_avatar = author.display_avatar

            embed.set_author(name=username, icon_url=user_avatar)

            await channel.send(embed=embed)


def setup(bot: Ezar):
    bot.add_cog(MessageLogs(bot))
