import datetime
from typing import Optional, Union

from disnake import Colour, Embed

from ezar.backend.config import Colors


class Embeb(Embed):
    """An `Embed` subclass to add default things, instead of having to manually configure them on each function."""

    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[Union[Colour, int]] = None,
        timestamp: Optional[datetime.datetime] = None,
        success: bool = False,
        failure: bool = False,
    ):
        super().__init__(
            title=title,
            description=description,
            url=url,
            color=color,
            timestamp=timestamp,
        )
        self.success = success
        self.failure = failure

        self.color = (
            color
            if color
            else Colors.green
            if self.success
            else Colors.red
            if self.failure
            else Colors.purple
        )
