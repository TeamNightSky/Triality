"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""
import typing as t

from discord import User as DiscordUser
from discord.ext.commands.errors import UserInputError

from triality.errors import NotEnoughMoney, RankNotExistError
from triality.models.money import Rank
from triality.models.user import User
from triality.utils import steal_percentage, steal_probability, weighted_random_bool

from .storage import StorageClient


class StorageManager(StorageClient):
    async def _basic_check(self, user: DiscordUser, amount: int, account: str) -> User:
        """For beginning of most functions"""
        db_user = await self.bot.storage.get_user(user)
        if 0 > amount > getattr(db_user.money, account).coins:
            if amount > 0:
                raise NotEnoughMoney(user, amount)
            else:
                raise UserInputError("Cannot withdraw negative coins")
        return db_user

    async def move_money_purse_to_bank(
        self, user: DiscordUser, amount: int, db_user: User
    ) -> None:
        """No checking"""
        db_user.money.bank.coins += amount
        db_user.money.purse.coins -= amount
        await db_user.sync_changes(self)

    async def add_user_money(self, amount: int, db_user: User, account: str) -> None:
        """No checking"""
        money = getattr(db_user.money, account).coins
        money += amount
        await db_user.sync_changes(self)

    async def transfer_money(
        self, sender: DiscordUser, recipient: DiscordUser, amount: int
    ):
        db_user = await self._basic_check(sender, amount, "purse")
        recip = await self.get_user(recipient)
        await self.add_user_money(-amount, db_user, "purse")
        await self.add_user_money(amount, recip, "purse")
        return db_user, recip

    async def withdraw(self, user: DiscordUser, amount: int) -> User:
        db_user = await self.bot.storage.get_user(user)
        if 0 > amount > db_user.money.bank.coins:
            if amount > 0:
                raise NotEnoughMoney(user, amount)
            else:
                raise UserInputError("Cannot withdraw negative coins")
        await self.move_money_purse_to_bank(user, -amount, db_user)
        return db_user

    async def deposit(self, user: DiscordUser, amount: int) -> User:
        db_user = await self.bot.storage.get_user(user)
        if 0 > amount > db_user.money.purse.coins:
            if amount > 0:
                raise NotEnoughMoney(user, amount)
            else:
                raise UserInputError("Cannot deposit negative coins")
        await self.move_money_purse_to_bank(user, amount, db_user)
        return db_user

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

    async def steal(self, user: DiscordUser, target: DiscordUser) -> t.Tuple[bool, int]:
        target_db_user = await self.bot.storage.get_user(target)
        db_user = await self.bot.storage.get_user(user)
        total = db_user.money.purse.coins + db_user.money.bank.coins

        weight = steal_probability(total, target_db_user.money.purse.coins)
        percentage = steal_percentage(total, target_db_user.money.purse.coins)

        if weighted_random_bool(weight):
            amount = int(percentage * target_db_user.money.purse.coins)
            db_user.money.purse.coins += amount
            target_db_user.money.purse.coins -= amount
            return True, amount
        else:
            return False, 0

    async def work(self, user: DiscordUser) -> User:
        db_user = await self.bot.storage.get_user(user)
        db_user.money.purse.coins += db_user.money.rank.salary
        return db_user
