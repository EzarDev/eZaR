from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from disnake import (
    CmdInter,
    MessageInteraction,
    NewsChannel,
    Permissions,
    SelectOption,
    TextChannel,
    Thread,
    VoiceChannel,
)
from disnake.abc import Messageable
from disnake.ext.commands import Cog, slash_command
from disnake.ui import Select, View

from ezar import Ezar
from ezar.backend.config import Database
from ezar.helpers.components import disable_components

if TYPE_CHECKING:
    from enum import Enum
    from typing import TypedDict

    class LoggingConfig(TypedDict):
        _id: int
        channel: int
        config: dict[str, bool]


__all__ = (
    "query_config",
    "query_config",
    "PLAIN_HANDLER",
    "UNIT_HANDLER",
    "ENUM_HANDLER",
    "NAMED_SNOWFLAKE_HANDLER",
    "INDEX_HANDLER",
)


PLAIN_HANDLER: Callable[[Any], str] = lambda p: f"`{p}`"
ENUM_HANDLER: Callable[[Enum], str] = lambda e: f"`{e.name.replace('_', ' ').title()}`"
UNIT_HANDLER: Callable[[str], Callable[[int], str]] = lambda u: lambda s: f"`{s}{u}`"
NAMED_SNOWFLAKE_HANDLER: Callable[[Any], str] = lambda s: f"`{s.name}` (`{s.id}`)"
INDEX_HANDLER: Callable[[int], str] = lambda i: f"`{i + 1}`"
LOG_TYPES: dict[str, str] = {
    # messages.py
    "message_edit": "Message Edits",
    "message_delete": "Message Deletes",
    "bulk_message_delete": "Bulk Message Deletes",
    # channels.py
    "guild_channel_create": "Channel Creates",
    "guild_channel_update": "Channel Edits",
    "guild_channel_delete": "Channel Deletes",
    # threads.py
    "thread_create": "Thread Creates",
    "thread_update": "Thread Edits",
    "thread_delete": "Thread Deletes",
    # emotes.py
    "guild_emojis_update": "Emoji Edits",
    "guild_stickers_update": "Sticker Edits",
    # invites.py
    "invite_create": "Invite Creates",
    "invite_delete": "Invite Deletes",
    # members.py
    "member_join": "Member Joins",
    "member_remove": "Member Leaves",
    # roles.py
    "guild_role_create": "Role Creates",
    "guild_role_delete": "Role Deletes",
    "guild_role_update": "Role Edits",
}
FALSE_LOG_TYPES = {k: False for k in LOG_TYPES}


async def query_config(
    *, bot: Ezar, guild_id: int, event: str
) -> Optional[Messageable]:
    document: Optional[LoggingConfig] = await Database.logs.find_one(  # type: ignore
        {"_id": guild_id, f"config.{event}": True}
    )

    if document is None:
        return None

    channel_id = document["channel"]

    return bot.get_partial_messageable(channel_id)


def parse_update(
    handlers: dict[str, Callable[[Any], str]], before: Any, after: Any
) -> str:
    changes: list[str] = []

    # Go through all checkable, make sure the human readables are not equal.
    # Except to handle if that attribute is not on this type.
    for attribute, modifier in sorted(handlers.items()):
        try:
            before_change = modifier(getattr(before, attribute))
            after_change = modifier(getattr(after, attribute))
        except AttributeError:
            continue
        else:
            if before_change != after_change:
                attr_fmt = attribute.replace("_", " ").title()
                changes.append(f"`{attr_fmt}` - {before_change} -> {after_change}")

    return "\n".join(changes)


class LogSelection(Select["LogSelectionView"]):
    def __init__(self, config: dict[str, bool]):
        super().__init__(
            min_values=1,
            max_values=len(LOG_TYPES),
            options=[
                SelectOption(label=v, value=k, default=config[k])
                for k, v in LOG_TYPES.items()
            ],
        )

    async def callback(self, interaction: MessageInteraction):
        await disable_components(view=self.view, itr=interaction)
        self.view.stop()


class LogSelectionView(View):
    interaction: CmdInter

    def __init__(self, config: dict[str, bool]):
        super().__init__()
        self.select = LogSelection(config)
        self.add_item(self.select)

    async def on_timeout(self) -> None:
        return await disable_components(
            self,
            new_content="You took too long to respond!",
            itr=self.interaction,
            as_response=False,
        )


class Logs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot
        self.db = Database.logs

    @slash_command(
        dm_permission=False, default_member_permissions=Permissions(manage_guild=True)
    )
    async def logs(self, inter: CmdInter):
        """Logging-related commands."""

    @logs.sub_command()
    async def subscribe(
        self,
        inter: CmdInter,
        channel: Union[TextChannel, VoiceChannel, Thread, NewsChannel],
    ):
        """Enable logging or modify your current configuration."""

        assert inter.guild is not None

        enabled = await self.db.find_one_and_delete({"_id": inter.guild.id})
        config = (
            enabled["config"]
            if (enabled is not None and enabled["channel"] == channel.id)
            else FALSE_LOG_TYPES
        )

        view = LogSelectionView(config)
        view.interaction = inter

        await inter.response.send_message("Select your preferred log types.", view=view)

        await view.wait()

        config = FALSE_LOG_TYPES | {v: True for v in view.select.values}
        await self.db.insert_one(
            {
                "_id": inter.guild.id,
                "channel": channel.id,
                "config": config,
            }
        )  # type: ignore
        await inter.response.send_message(
            "Your selected log events have been configured for this server!"
        )

    @logs.sub_command()
    async def disable(self, inter: CmdInter):
        """Disable logging for this server."""

        assert inter.guild is not None
        await self.db.delete_one({"_id": inter.guild.id})  # type: ignore
        await inter.response.send_message("Logging has been disabled for this server.")


def setup(bot: Ezar):
    bot.add_cog(Logs(bot))
