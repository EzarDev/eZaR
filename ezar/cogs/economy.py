from datetime import datetime
from typing import Optional

from disnake import (
    ApplicationCommandInteraction,
    InteractionMessage,
    Member,
    MessageInteraction,
    User,
)
from disnake.ext.commands import Cog, slash_command
from disnake.ui import Button, View, button

from ezar import Ezar
from ezar.backend.config import Database, Emojis
from ezar.helpers.components import disable_components
from ezar.utils.embed import Embeb


class ProfileCreate(View):
    def __init__(self, author: Member):
        self.db = Database.economy
        self.author = author
        self.message: InteractionMessage
        super().__init__(timeout=60)

    async def on_timeout(self) -> None:
        return await disable_components(
            self, new_content="You took too long to respond!", message=self.message
        )

    @button(label="Yes, I agree", emoji=Emojis.tick)
    async def create_agree(self, button: Button, itr: MessageInteraction) -> None:
        if not itr.author.id == self.author.id:
            return await itr.response.send_message(
                f"{Emojis.cross} You are not the author of this command.",
                ephemeral=True,
            )

        await self.db.insert_one(
            {
                "_id": itr.user.id,
                "created_at": datetime.now().timestamp(),
                "cash": 0,
                "bank_cash": 0,
            }
        )
        await disable_components(
            self,
            itr=itr,
            new_content=f"{Emojis.tick} You have created an account! Run `/eco job get` to get a job.",
        )
        self.stop()
        return

    @button(label="No, I do not agree", emoji=Emojis.cross)
    async def create_disagree(self, button: Button, itr: MessageInteraction) -> None:
        if not itr.author.id == self.author.id:
            return await itr.response.send_message(
                f"{Emojis.cross} You are not the author of this command.",
                ephemeral=True,
            )
        await disable_components(self, itr=itr)
        self.stop()
        return


class Economy(Cog):
    def __init__(self, bot: Ezar):
        self.bot = bot
        self.db = Database.economy

    @slash_command()
    async def eco(self, itr: ApplicationCommandInteraction):
        """Economy-related commands"""

    @eco.sub_command_group("profile")
    async def eco_profile(self, itr: ApplicationCommandInteraction):
        """Economy-profile-related commands"""

    @eco_profile.sub_command("create")
    async def eco_profile_create(self, itr: ApplicationCommandInteraction):
        """Create a profile on the economy system."""
        check = await self.db.find_one({"_id": itr.user.id})
        if check:
            return await itr.response.send_message(
                f"{Emojis.cross} You already have an account.", ephemeral=True
            )
        else:
            view = ProfileCreate(itr.user)
            await itr.response.send_message(
                "<ToS placeholder>", view=view
            )  # TODO: make a ToS for this
            view.message = await itr.original_message()
            return

    @eco_profile.sub_command("show")
    async def eco_profile_show(
        self, itr: ApplicationCommandInteraction, user: Optional[User] = None
    ):
        """View a person's profile.

        Parameters
        ----------
        user: The user to view."""
        if not user:
            user: Member = itr.user

        check = await self.db.find_one({"_id": user.id})
        if not check:
            error_msg = " not have a profile"
            await itr.response.defer()
            return await itr.edit_original_message(
                "You do" + error_msg
                if not check and user == itr.user
                else f"{user} does" + error_msg
            )

        name = user.name if not user.nick else f"{user.name} ({str(user.nick)!r})"
        total = check["cash"] + check["bank_cash"]
        wealth = (
            "Broke as hell"
            if total < 300
            else "Has a decent amount of money"
            if total < 1000
            else "Rich AF"
        )

        prof_embed = Embeb(
            color=user.colour,
            title=name,
            description=wealth,
            timestamp=datetime.fromtimestamp(check["created_at"]),
        )
        prof_embed.set_thumbnail(user.display_avatar.url)
        prof_embed.add_field(name="Total Cash Amount", value=total)
        prof_embed.add_field(name="Cash", value=check["cash"])
        prof_embed.add_field(name="Credit", value=check["bank_cash"])
        prof_embed.set_footer(text="Account created at")
        return await itr.response.send_message(embed=prof_embed)


def setup(bot: Ezar):
    bot.add_cog(Economy(bot))
