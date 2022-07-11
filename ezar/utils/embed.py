import datetime
from typing import Optional

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
        color: Optional[int | Colour] = None,
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
            Colors.purple
            if not self.success and self.color is None
            else Colors.green
            if not self.failure and self.color is None
            else Colors.red
        )
