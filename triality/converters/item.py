"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

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
