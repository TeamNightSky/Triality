import typing as t

import discord
from discord.ext.commands import Cog, Context  # type: ignore[attr-defined]

if t.TYPE_CHECKING:
    from ..bot import Triality


class Money(Cog):
    async def bank(self, ctx: Context, user: t.Optional[discord.User] = None) -> None:
        if user is None:
            user = ctx.message.author
        db_user = await self.bot.storage.get_user(user)
        await ctx.send(db_user.bank.coins)

    async def purse(self, ctx: Context, user: t.Optional[discord.User] = None) -> None:
        if user is None:
            user = ctx.message.author
        db_user = await self.bot.storage.get_user(user)
        await ctx.send(db_user.purse.coins)

    async def deposit(self, ctx: Context, amount: int) -> None:
        user = ctx.message.author
        db_user = await self.bot.storage.get_user(user)
        if 0 < amount <= db_user.purse.coins:
            db_user.bank.coins += amount
            db_user.purse.coins -= amount
            await db_user.sync_changes()
            await ctx.send(f"Your bank now has {db_user.bank.coins} coins")
        else:
            await ctx.send("Invalid amount")

    async def withdraw(self, ctx: Context, amount: int) -> None:
        user = ctx.message.author
        db_user = await self.bot.storage.get_user(user)
        if 0 < amount <= db_user.bank.coins:
            db_user.purse.coins += amount
            db_user.bank.coins -= amount
            await db_user.sync_changes()
            await ctx.send(f"Your purse now has {db_user.purse.coins} coins")
        else:
            await ctx.send("Invalid amount")


def setup(bot: "Triality") -> None:
    bot.add_cog(Money(bot))
