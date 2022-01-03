"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

from discord import User
from discord.ext.commands import (  # type: ignore[attr-defined]
    CommandError,
    UserInputError,
)


class Error(Exception):
    pass


class DatabaseError(Error):
    pass


class ItemNotFound(UserInputError):
    pass


class NotEnoughMoney(UserInputError):
    def __init__(self, user: User, amount: int):
        self.user = user
        self.amount = amount
        super().__init__(f"{user.name} doesn't have {amount} coins")


class NotEnoughItems(UserInputError):
    def __init__(self, user: User, item: str, amount: int):
        self.user = user
        self.item = item
        self.amount = amount
        super().__init__(f"{user.name} doesn't have {amount}x {item}/s")


class NotEnoughSpace(UserInputError):
    def __init__(self, space: str, max: int, amount: int):
        self.space = space
        self.max = max
        self.amount = amount
        super().__init__(f"{space} can't fit {amount}, only {max} spaces remaining")


class ItemNotPlantable(UserInputError):
    def __init__(self, item: str):
        self.item = item
        super().__init__(f"{item} is not plantable")


class RankNotExistError(CommandError):
    pass
