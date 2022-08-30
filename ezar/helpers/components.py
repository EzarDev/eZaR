from typing import Optional, Union

from disnake import Interaction, InteractionMessage, Message
from disnake.ui import View
from disnake.utils import MISSING


async def disable_components(
    view: View,
    *,
    new_content: Optional[str] = MISSING,
    message: Optional[Union[InteractionMessage, Message]] = None,
    itr: Optional[Interaction] = None,
    as_response: bool = True
) -> None:
    """Disables all components(buttons, selects, etc.) in messages.

    Parameters
    ----------
    view: :class:`disnake.ui.View`
        The view with the components to disable.
    new_content: Optional[:class:`str`]
        The new message content.
    message: Optional[:class:`InteractionMessage | Message`]
        The message to edit.
    itr: Optional[:class:`Interaction`]
        The interaction.
    as_response: :class:`bool`
        If this should be the response to the interaction, or use it to edit the response.
    """
    for items in view.children:
        items.disabled = True
    if not message:
        if not itr:
            raise ValueError("Must pass either `message` or `itr`")
        else:
            if as_response:
                await itr.response.edit_message(new_content, view=view)
            else:
                await itr.edit_original_message(new_content, view=view)
    else:
        if new_content:
            await message.edit(new_content, view=view)
            return
        else:
            await message.edit(view=view)
            return
