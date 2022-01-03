"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import os

import discord

from .const import DESCRIPTION, MAX_MESSAGES, OWNER_ID
from .core.bot import Triality

bot = Triality(
    description=DESCRIPTION,
    owner_id=OWNER_ID,
    max_messages=MAX_MESSAGES,
    command_prefix=".",
    help_command=None,
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="Screams of the Devil",
    ),
    status=discord.Status.online,
)


if __name__ == "__main__":
    bot.run(os.getenv("BOT_TOKEN"))
