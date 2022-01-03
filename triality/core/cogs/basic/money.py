import math
import random
import typing as t

import discord
from discord.commands import ApplicationContext, slash_command
from discord.ext.commands import (  # type: ignore[attr-defined]
    BucketType,
    Cog,
    UserInputError,
    cooldown,
)

from triality.const import (
    DEV_SERVERS,
    EMPTY_STEAL_MESSAGES,
    FAVOR_MESSAGES,
    GIVE_MESSAGES,
    PROMOTED_MESSAGES,
    RANDOM_WEIGHT_ACCURACY,
    STEAL_FAIL_MESSAGES,
    STEAL_SUCCESS_MESSAGES,
    WORK_MESSAGES,
)
from triality.core.bot import Triality
from triality.errors import RankNotExistError
from triality.models.money import Rank
from triality.models.user import User
from triality.utils import Field


def steal_probability(user_coins: int, target_coins: int) -> float:
    return 1 / ((user_coins / (target_coins / 2 + 1)) ** 2 + 1)


def steal_percentage(user_coins: int, target_coins: int) -> float:
    if user_coins > 2 * target_coins:
        return 0
    return math.cos(math.pi * user_coins / (4 * target_coins))


def weighted_random_bool(weight: float) -> bool:
    choices = (True, False)
    weights = (weight * RANDOM_WEIGHT_ACCURACY, (1 - weight) * RANDOM_WEIGHT_ACCURACY)
    choice, *_ = random.choices(choices, weights=weights)
    return choice


class Money(Cog):
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
            ctx, title=f"{user.display_name}'s Money", fields=[bank, purse, salary]
        )

    @slash_command(guild_ids=DEV_SERVERS)
    async def deposit(self, ctx: ApplicationContext, amount: t.Union[str, int]) -> None:
        """Deposit :moneybag: to your bank"""
        db_user = await self.bot.storage.get_user(ctx.user)
        if amount == "all":
            amount = db_user.money.purse.coins
        elif not isinstance(amount, int):
            raise UserInputError("Amount must either be either ``all`` or a integer.")
        if 0 < amount <= db_user.money.purse.coins:
            db_user.money.bank.coins += amount
            db_user.money.purse.coins -= amount
            await db_user.sync_changes(self.bot.storage)
            await self.bot.embed_response(
                ctx,
                f"Your bank now has :moneybag: {db_user.money.bank.coins}",
            )
        else:
            raise UserInputError(
                f"Invalid amount, must be between 0 and {db_user.money.purse.coins}"
            )

    @slash_command(guild_ids=DEV_SERVERS)
    async def withdraw(
        self, ctx: ApplicationContext, amount: t.Union[str, int]
    ) -> None:
        """Withdraw :moneybag: to your purse"""
        db_user = await self.bot.storage.get_user(ctx.user)
        if amount == "all":
            amount = db_user.money.bank.coins
        elif not isinstance(amount, int):
            raise UserInputError("Amount must either be either ``all`` or a integer.")
        if 0 < amount <= db_user.money.bank.coins:
            db_user.money.purse.coins += amount
            db_user.money.bank.coins -= amount
            await db_user.sync_changes(self.bot.storage)
            await self.bot.embed_response(
                ctx, f"Your purse now has :moneybag: {db_user.money.purse.coins}"
            )
        else:
            raise UserInputError(
                f"Invalid amount, must be between 0 and {db_user.money.bank.coins}"
            )

    @slash_command(guild_ids=DEV_SERVERS)
    @cooldown(rate=1, per=60 * 60, type=BucketType.user)
    async def work(self, ctx: ApplicationContext) -> None:
        """Work at a job for a salary."""
        db_user = await self.bot.storage.get_user(ctx.user)
        db_user.money.purse.coins += db_user.money.rank.salary
        await self.bot.embed_response(
            ctx,
            title=random.choice(WORK_MESSAGES),
            image_url=db_user.money.rank.image,
            content=f"You worked and received your salary of :moneybag: {db_user.money.rank.salary}. Your purse now has :moneybag: {db_user.money.purse.coins}",
        )
        weight = db_user.money.rank.promotion_chance_increase
        db_user.money.rank.progress += weight
        if weighted_random_bool(db_user.money.rank.progress):
            await self.promote_user(db_user)
            await self.bot.embed_response(
                ctx,
                title=random.choice(PROMOTED_MESSAGES),
                content="You were promoted to {Insert Rank Here}",
                follow_up=True,
                image_url=db_user.money.rank.image,
            )
        await db_user.sync_changes(self.bot.storage)

    async def promote_user(self, db_user: User) -> None:
        level = db_user.money.rank.level
        data = await self.bot.storage.get_from_table("Ranks", ["*"], level=level + 1)
        try:
            rank, *_ = data
        except ValueError:
            raise RankNotExistError(
                f"There is no rank after ``{db_user.money.rank.title}``"
            )
        db_user.money.rank = Rank(**rank)

    @slash_command(guild_ids=DEV_SERVERS)
    @cooldown(rate=1, per=60 * 60, type=BucketType.user)
    async def favor(self, ctx: ApplicationContext) -> None:
        """Do a favor for someone because you are nice! :D"""
        await ctx.respond(random.choice(FAVOR_MESSAGES))

    @slash_command(guild_ids=DEV_SERVERS)
    @cooldown(rate=1, per=60 * 60 * 24, type=BucketType.user)
    async def steal(self, ctx: ApplicationContext, user: discord.User) -> None:
        """Steal some money from someone purse! >:)"""
        target_db_user = await self.bot.storage.get_user(user)
        db_user = await self.bot.storage.get_user(ctx.user)
        total = db_user.money.purse.coins + db_user.money.bank.coins

        weight = steal_probability(total, target_db_user.money.purse.coins)
        percentage = steal_percentage(total, target_db_user.money.purse.coins)

        if weighted_random_bool(weight):
            amount = t.cast(int, int(percentage * target_db_user.money.purse.coins))
            db_user.money.purse.coins += amount
            target_db_user.money.purse.coins -= amount
            await target_db_user.sync_changes(self.bot.storage)
            await db_user.sync_changes(self.bot.storage)
            if amount == 0:
                title = random.choice(EMPTY_STEAL_MESSAGES)
            else:
                title = random.choice(STEAL_SUCCESS_MESSAGES)
            await self.bot.embed_response(
                ctx,
                title=title,
                content=f"You stole :moneybag: {amount} from {user.mention}. Your purse now has :moneybag: {db_user.money.purse.coins}.",
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
        self, ctx: ApplicationContext, user: discord.User, amount: t.Union[str, int]
    ) -> None:
        """Give someone money from your purse because you like them! :D"""
        target_db_user = await self.bot.storage.get_user(user)
        db_user = await self.bot.storage.get_user(ctx.user)
        if amount == "all":
            amount = db_user.money.purse.coins
        elif not isinstance(amount, int):
            raise UserInputError("Amount must either be either ``all`` or a integer.")
        if 0 <= amount <= db_user.money.purse.coins:
            db_user.money.purse.coins -= amount
            target_db_user.money.bank.coins += amount
            await db_user.sync_changes(self.bot.storage)
            await target_db_user.sync_changes(self.bot.storage)
            await self.bot.embed_respone(
                ctx,
                title=random.choice(GIVE_MESSAGES),
                content=f"You gave {user.display_name} :moneybag: {amount}. Your purse no has :moneybag: 0",
            )
        elif amount < 0:
            raise UserInputError(
                "Bruh, you cannot give people a negative amount of :moneybag: lol. Try again."
            )
        elif amount > db_user.money.purse.coins:
            raise UserInputError(
                f"You do not have enough :moneybag: in your purse to give {user.display_name} {amount} :moneybag:"
            )


def setup(bot: "Triality") -> None:
    bot.add_cog(Money(bot))
