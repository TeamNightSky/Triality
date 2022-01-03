from discord.commands import ApplicationContext
from discord.ext.commands import Converter  # type: ignore[attr-defined]

from triality.errors import ItemNotFound
from triality.models.items import Item


class ItemConverter(Converter):
    @classmethod
    async def convert(cls, ctx: ApplicationContext, argument: str) -> Item:
        result = await ctx.bot.storage.get_item(slug=argument)  # type: ignore[attr-defined]
        if result is None:
            raise ItemNotFound(argument)
        return result
