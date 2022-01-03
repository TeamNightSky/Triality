"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

from datetime import datetime, timedelta

from discord.commands import ApplicationContext, SlashCommandGroup  # type: ignore
from discord.ext.commands import Cog, UserInputError  # type: ignore[attr-defined]

from triality import const
from triality.converters import ItemConverter
from triality.core.bot import Triality
from triality.errors import (
    ItemNotFound,
    ItemNotPlantable,
    NotEnoughItems,
    NotEnoughSpace,
)
from triality.models import Crop
from triality.utils import Field, format_delta


def setup(bot: Triality) -> None:
    bot.add_cog(Farming(bot))


class Farming(Cog):
    group = SlashCommandGroup("farm", "Plant, Harvest and view crops in your Farm.")

    def __init__(self, bot: Triality):
        self.bot = bot

    @group.command(guild_ids=const.DEV_SERVERS)
    async def plant(
        self,
        ctx: ApplicationContext,
        seed: ItemConverter,
        amount: int = 1,
    ) -> None:
        """Plant seeds in your farm"""
        db_user = await self.bot.storage.get_user(ctx.user)

        if not db_user.inventory.items.get(seed.slug, 0):
            raise ItemNotFound(seed.name)
        if not seed.settings.farming.plantable:
            raise ItemNotPlantable(seed.name)
        if db_user.inventory.items[seed.slug] < amount:
            raise NotEnoughItems(ctx.author, seed.name, amount)
        if amount <= 0:
            raise UserInputError("Amount must be above 0")

        max = db_user.farm.max_in_progress
        current = db_user.farm.in_progress

        if len(current) + amount > max:
            raise NotEnoughSpace("Farm", max - len(current), amount)

        db_user.inventory.items[seed.slug] -= amount
        for i in range(amount):
            timediff = timedelta(seconds=seed.settings.farming.grow_time)
            db_user.farm.in_progress.append(
                Crop(
                    planted_seed=seed.slug,
                    end=datetime.utcnow() + timediff,
                )
            )

        await self.bot.embed_response(ctx, f"Planted {amount}x {seed.name}")

    @group.command(guild_ids=const.DEV_SERVERS)
    async def harvest(self, ctx: ApplicationContext) -> None:
        """Harvest all of your fully grown crops"""
        # db_user = await self.bot.storage.get_user(ctx.user)

    @group.command(guild_ids=const.DEV_SERVERS)
    async def view(self, ctx: ApplicationContext):
        """View the crops that you have planted."""
        db_user = await self.bot.storage.get_user(ctx.user)

        crops = db_user.farm.in_progress
        fields = []

        for crop in crops:
            growing = crop.end - datetime.utcnow()
            if growing.total_seconds() < 0:
                growing = "*Done*"
            else:
                left = format_delta(growing)
                if crop.last_watered is not None:
                    last = datetime.utcnow() - crop.last_watered
                    watered = f"\nLast watered at *{format_delta(last)}*"
                else:
                    watered = ""
                growing = f"*{left}* until grown.{watered}"
            fields.append(Field(crop.planted_seed.replace("-", " ").title(), growing))

        if not fields:
            fields = [Field("No crops here :(", "Use `/farm plant` to plant some!")]

        await self.bot.embed_response(ctx, "Your crops", fields=fields)
