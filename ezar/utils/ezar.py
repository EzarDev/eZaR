from datetime import datetime

from disnake import Activity, ActivityType, AllowedMentions, Intents, MemberCacheFlags
from disnake.ext.commands import Bot

from ezar.backend.config import Config


class Ezar(Bot):
    def __init__(self, *, beta: bool = True):
        self.beta = beta
        self.start_time: datetime
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
            member_cache_flags=MemberCacheFlags(voice=False),
        )

    async def login(self, token: str):
        self.start_time = datetime.now()
        return await super().login(token)
