from disnake import (
    Activity,
    ActivityType,
    AllowedMentions,
    HTTPException,
    Intents,
    NotFound,
)
from disnake.ext.commands import Bot

from ezar.backend.config import Config


class Ezar(Bot):
    def __init__(self, *, beta: bool = True):
        self.beta = beta
        super().__init__(
            "$",
            None,
            case_insensitive=True,
            owner_ids=Config.owner_ids,
            reload=True,
            strip_after_prefix=True,
            sync_commands=True,
            sync_commands_on_unload=True,
            test_guilds=(Config.test_guilds,) if self.beta else [],
            intents=Intents(
                message_content=True, guilds=True, members=True, messages=True
            ),
            activity=Activity(name="Stuff", type=ActivityType.watching),
            allowed_mentions=AllowedMentions(everyone=False, users=True, roles=False),
        )

    async def getch_channel(self, channel_id: int):
        """Returns a Discord channel with the given ID. Gets channel at first, fetches channel if it fails

        Parameters
        ----------
        channel_id: :class:`int`
            The channel ID"""
        try:
            return self.get_channel(channel_id)
        except (NotFound, HTTPException):
            return await self.fetch_channel(channel_id)
