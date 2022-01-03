"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

from discord.commands import ApplicationContext  # type: ignore
from discord.ext.commands import Cog, UserInputError  # type: ignore[attr-defined]

from triality.utils import Field

from ..bot import Triality


def setup(bot: Triality):
    bot.add_cog(ErrorHandler(bot))


class ErrorHandler(Cog):
    def __init__(self, bot: Triality):
        self.bot = bot

    @Cog.listener(name="on_command_error")
    async def error_listener(self, ctx: ApplicationContext, error: Exception):
        if isinstance(error, UserInputError):
            await self.user_input_error(ctx, error)
        else:
            self.bot.log.error(
                "%s caused %s", ctx.message.content, error, exc_info=error
            )

    async def user_input_error(self, ctx: ApplicationContext, error: Exception) -> None:
        c = self.bot.get_command(ctx.message.content[1:].split(" ")[0])
        proper = Field(
            "Proper Usage",
            f'`{" " + " ".join([i.name for i in c.parents]) if c.parents else ""}{c.name}{" "+ c.signature if c.signature else ""}`',
        )
        await self.bot.embed_response(
            ctx,
            "User input error",
            str(error),
            fields=[proper],
            success=False,
        )
