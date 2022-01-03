"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import logging

from discord.commands import SlashCommandGroup  # type: ignore
from discord.ext.commands import Cog, Context  # type: ignore[attr-defined]

from triality.const import DEV_SERVERS

from ..bot import Triality


def setup(bot: Triality):
    bot.add_cog(Sudo(bot))


class Sudo(Cog):
    group: SlashCommandGroup = SlashCommandGroup(
        "sudo", "Developer tools for the bot developers."
    )

    def __init__(self, bot: Triality) -> None:
        self.bot = bot

    levels = {
        1: "DEBUG",
        2: "INFO",
        3: "WARNING",
        4: "ERROR",
        5: "CRITICAL",
    }

    @group.command(guild_ids=DEV_SERVERS)
    async def loglevel(self, ctx: Context, level: int) -> None:
        """Set the log level. `level` param is level starting at debug (1: debug, 2: info, etc.)"""
        self.bot.log.info("Changing log level to %s", Sudo.levels[level])
        if level > 2:
            self.bot.log.warning(
                "A log level above 1 will not display all important information. Setting level to %s",
                Sudo.levels[level],
            )
        loglevel = getattr(logging, Sudo.levels.get(level, "DEBUG"))
        self.bot.log.setLevel(loglevel)
        await self.bot.embed_response(ctx, f"Set log level to {Sudo.levels[level]}")
