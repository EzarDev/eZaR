from disnake import (
    ApplicationCommandInteraction,
    InteractionMessage,
    Member,
    MessageInteraction,
)
from disnake.ext.commands import Cog, slash_command
from disnake.ui import Button, View, button

from ezar import Ezar
from ezar.backend.config import Database, Emojis
from ezar.helpers.components import disable_components


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
    async def create_agree(self, button: MessageInteraction, itr: Button) -> None:
        if not itr.author.id == self.author.id:
            return await itr.response.send_message(
                f"{Emojis.cross} You are not the author of this command.",
                ephemeral=True,
            )

        await self.db.insert_one({"_id": itr.user.id, "cash": 0, "bank_cash": 0})
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


def setup(bot: Ezar):
    bot.add_cog(Economy(bot))
