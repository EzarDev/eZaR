import datetime
from disnake import Colour, Embed

from ezar.backend.config.constants import Colors


class Embeb(Embed):
    """An `Embed` subclass to add default things, instead of having to manually configure them on each function."""

    def __init__(
        self,
        *,
        title: str = None,
        description: str = None,
        url: str = None,
        color: int | Colour = None,
        timestamp: datetime.datetime = None,
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
