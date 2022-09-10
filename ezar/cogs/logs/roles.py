from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any, Callable

from disnake.ext.commands import Cog

from ezar.cogs.logs import INDEX_HANDLER, PLAIN_HANDLER, parse_update, query_config
from ezar.utils.embed import Embeb

if TYPE_CHECKING:
    from disnake import Role

    from ezar import Ezar


log = getLogger(__name__)
UPDATE_HANDLERS: dict[str, Callable[[Any], str]] = {
    "colour": PLAIN_HANDLER,
    "emoji": PLAIN_HANDLER,
    "hoist": PLAIN_HANDLER,
    "icon": lambda i: i.url if i else "None",
    "managed": PLAIN_HANDLER,
    "mentionable": PLAIN_HANDLER,
    "name": PLAIN_HANDLER,
    "permissions": lambda p: ", ".join(
        f"`{perm.replace('_', ' ').title()}`" for perm, enabled in sorted(p) if enabled
    ),
    "position": INDEX_HANDLER,
}
ROLE_EDITED = """

{role.mention} (`{role.name}` - `{role.id}`) was edited.

**Changes**:
{changed}

""".strip()


class RoleLogs(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot

    @Cog.listener()
    async def on_guild_role_create(self, role: Role):
        guild = role.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_role_create"
        ):
            description = (
                f"{role.mention} (`{role}` - `{role.id}`) was created "
                f"with the colour #{hex(role.colour.value)[2:].ljust(6, '0')}."
                f" It has position {role.position + 1}. It is "
                + ("hoisted" if role.hoist else "not hoisted")
                + " and "
                + ("mentionable" if role.mentionable else "not mentionable")
            )

            perms = [
                f"`{r[0].replace('_', ' ').title()}`"
                for r in filter(lambda r: r[1], role.permissions)
            ]
            permission_desc = (
                ", ".join(perms) + " permissions" if perms else " no permissions"
            )
            description += f" and has {permission_desc}."

            embed = Embeb(title="Role Created", description=description, success=True)
            await channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_role_update(self, before: Role, after: Role):
        guild = after.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_role_update"
        ):
            changes = parse_update(handlers=UPDATE_HANDLERS, before=before, after=after)

            if changes:
                embed = Embeb(
                    title="Role Edited",
                    description=ROLE_EDITED.format(role=after, changed=changes),
                )
                await channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_role_delete(self, role: Role):
        guild = role.guild

        if channel := await query_config(
            bot=self.bot, guild_id=guild.id, event="guild_role_delete"
        ):
            embed = Embeb(
                title="Role Deleted",
                description=f"`{role}` (`{role.id}`) was deleted.",
                failure=True,
            )
            await channel.send(embed=embed)


def setup(bot: Ezar):
    bot.add_cog(RoleLogs(bot))
