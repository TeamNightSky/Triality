"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import typing as t

from discord.commands import ApplicationContext
from discord.ext.commands import Converter, UserInputError  # type: ignore[attr-defined]


class AmountConverter(Converter):
    def __init__(self, location: str) -> None:
        self.location = location

    async def convert(
        self, ctx: ApplicationContext, argument: t.Union[str, int]
    ) -> int:
        db_user = await ctx.bot.storage.get_user(ctx.user)  # type: ignore[attr-defined]
        if argument == "all":
            amount = getattr(db_user.money, self.location).coins
        elif not isinstance(amount, int):
            raise UserInputError("Amount must either be either ``all`` or a integer.")
        return amount
