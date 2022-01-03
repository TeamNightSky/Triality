"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import random
import typing as t

import discord
from discord.commands import ApplicationContext, slash_command  # type: ignore
from discord.ext.commands import BucketType, Cog, cooldown  # type: ignore[attr-defined]

from triality.const import (
    DEV_SERVERS,
    EMPTY_STEAL_MESSAGES,
    FAVOR_MESSAGES,
    GIVE_MESSAGES,
    PROMOTED_MESSAGES,
    STEAL_FAIL_MESSAGES,
    STEAL_SUCCESS_MESSAGES,
    WORK_MESSAGES,
)
from triality.converters import AmountConverter
from triality.core.bot import Triality
from triality.utils import Field, weighted_random_bool


class Money(Cog):
    BANK_AMOUNT: t.TypeAlias = AmountConverter("bank")
    PURSE_AMOUNT: t.TypeAlist = AmountConverter("purse")

    def __init__(self, bot: Triality):
        self.bot = bot

    @slash_command(guild_ids=DEV_SERVERS)
    async def money(
        self, ctx: ApplicationContext, user: t.Optional[discord.User] = None
    ) -> None:
        """View yours/a player's bank and purse"""
        user = user or ctx.user
        db_user = await self.bot.storage.get_user(user)
        bank = Field("Bank", f":moneybag: {db_user.money.bank.coins}")
        purse = Field("Purse", f":moneybag: {db_user.money.purse.coins}")
        salary = Field("Salary", f":moneybag: {db_user.money.rank.salary}")
        await self.bot.embed_response(
            ctx,
            title=f"{user.display_name}'s Money",
            fields=[bank, purse, salary],
            image_url=db_user.money.rank.image,
        )

    @slash_command(guild_ids=DEV_SERVERS)
    async def deposit(self, ctx: ApplicationContext, amount: PURSE_AMOUNT) -> None:
        """Deposit :moneybag: to your bank"""
        db_user = await self.bot.storage.deposit(ctx.user, amount)
        await self.bot.embed_response(
            ctx,
            f"Your bank now has :moneybag: {db_user.money.bank.coins}",
        )

    @slash_command(guild_ids=DEV_SERVERS)
    async def withdraw(self, ctx: ApplicationContext, amount: BANK_AMOUNT) -> None:
        """Withdraw :moneybag: to your purse"""
        db_user = await self.bot.storage.withdraw(ctx.user, amount)
        await self.bot.embed_response(
            ctx, f"Your purse now has :moneybag: {db_user.money.purse.coins}"
        )

    @slash_command(guild_ids=DEV_SERVERS)
    @cooldown(rate=1, per=60 * 60, type=BucketType.user)
    async def work(self, ctx: ApplicationContext) -> None:
        """Work at a job for a salary."""
        db_user = await self.bot.storage.work(ctx.user)
        await self.bot.embed_response(
            ctx,
            title=random.choice(WORK_MESSAGES),
            image_url=db_user.money.rank.image,
            content=f"You worked and received your salary of :moneybag: {db_user.money.rank.salary}. Your purse now has :moneybag: {db_user.money.purse.coins}",
        )

        weight = db_user.money.rank.promotion_chance_increase
        db_user.money.rank.progress += weight
        if weighted_random_bool(db_user.money.rank.progress):
            await self.bot.storage.promote_user(db_user)
            await self.bot.embed_response(
                ctx,
                title=random.choice(PROMOTED_MESSAGES),
                content=f"You were promoted to {db_user.money.rank.title}",
                follow_up=True,
                image_url=db_user.money.rank.image,
            )
        await db_user.sync_changes(self.bot.storage)

    @slash_command(guild_ids=DEV_SERVERS)
    @cooldown(rate=1, per=60 * 60, type=BucketType.user)
    async def favor(self, ctx: ApplicationContext) -> None:
        """Do a favor for someone because you are nice! :D"""
        await ctx.respond(random.choice(FAVOR_MESSAGES) % 0)

    @slash_command(guild_ids=DEV_SERVERS)
    @cooldown(rate=1, per=60 * 60 * 24, type=BucketType.user)
    async def steal(self, ctx: ApplicationContext, user: discord.User) -> None:
        """Steal some money from someone purse! >:)"""
        success, amount = await self.bot.storage.steal(ctx.user, user)

        if success:
            if amount == 0:
                title = random.choice(EMPTY_STEAL_MESSAGES)
            else:
                title = random.choice(STEAL_SUCCESS_MESSAGES) % amount
            await self.bot.embed_response(
                ctx,
                title=title,
                content=f"You stole :moneybag: {amount} from {user.mention}.",
            )
        else:
            await self.bot.embed_response(
                ctx,
                title=random.choice(STEAL_FAIL_MESSAGES),
                content=f"You failed to steal anything from {user.mention}.",
            )
        await user.send(f"{ctx.user} made a steal attempt against you!")

    @slash_command(guild_ids=DEV_SERVERS)
    async def give(
        self,
        ctx: ApplicationContext,
        user: discord.User,
        amount: PURSE_AMOUNT,
    ) -> None:
        """Give someone money from your purse because you like them! :D"""
        await self.bot.storage.transfer_money(ctx.author, user, amount)
        await self.bot.embed_response(
            ctx,
            title=random.choice(GIVE_MESSAGES) % 0,
            content=f"You gave {user.display_name} :moneybag: {amount}. Your purse no has :moneybag: 0",
        )


def setup(bot: "Triality") -> None:
    bot.add_cog(Money(bot))
