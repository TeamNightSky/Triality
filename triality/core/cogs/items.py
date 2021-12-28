import typing as t

from discord.ext.commands import Cog  # type: ignore[attr-defined]

if t.TYPE_CHECKING:
    from ..bot import Triality


class Inventory(Cog):
    def __init__(self, bot: "Triality") -> None:
        self.bot = bot


class Store(Cog):
    pass


def setup(bot: "Triality"):
    pass
