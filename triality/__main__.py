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
