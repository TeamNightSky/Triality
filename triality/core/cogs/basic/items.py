"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

from discord.commands import ApplicationContext, slash_command  # type: ignore
from discord.ext.commands import Cog  # type: ignore[attr-defined]

from triality import const
from triality.converters import ItemConverter
from triality.core.bot import Triality


class Inventory(Cog):
    def __init__(self, bot: Triality) -> None:
        self.bot = bot

    @slash_command(guild_ids=const.DEV_SERVERS)
    async def inventory(self, ctx: ApplicationContext):
        await self.bot.embed_response(ctx, "Fetching your inventory...")
        db_user = await self.bot.storage.get_user(ctx.user)
        await self.bot.embed_response(
            ctx,
            title="Your Inventory",
            content=str(db_user.inventory.items),
            follow_up=True,
        )

    async def spawn_artifacts(self):
        pass


class Market(Cog):
    def __init__(self, bot: Triality) -> None:
        self.bot = bot

    @slash_command(guild_ids=const.DEV_SERVERS)
    async def market(self, ctx: ApplicationContext):
        await ctx.respond("Hi!")

    @slash_command(guild_ids=const.DEV_SERVERS)
    async def item(self, ctx: ApplicationContext, item: ItemConverter):
        await ctx.respond(item.to_json_string())


def setup(bot: Triality) -> None:
    bot.add_cog(Inventory(bot))
    bot.add_cog(Market(bot))
