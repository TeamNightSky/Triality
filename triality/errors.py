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
    pass


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
