import os

import discord

from .const import DESCRIPTION, MAX_MESSAGES, OWNER_ID
from .core.bot import Triality

bot = Triality(
    description=DESCRIPTION,
    owner_id=OWNER_ID,
    max_messages=MAX_MESSAGES,
    command_prefix="\\/",  # For testing when slash commands are being slow/not working
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="Screams of the Devil",
    ),
    status=discord.Status.online,
)

bot.run(os.getenv("BOT_TOKEN"))
