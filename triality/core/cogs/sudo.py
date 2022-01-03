import logging

from discord.commands import SlashCommandGroup
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
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
        5: logging.CRITICAL,
    }

    @group.command(guild_ids=DEV_SERVERS)
    async def loglevel(self, ctx: Context, level: int) -> None:
        """Set the log level. `level` param is level starting at debug (1: debug, 2: info, etc.)"""
        self.bot.log.info("Changing log level to %s", level)
        if level > 1:
            self.bot.log.warning(
                "A log level above 1 will not display all important information. Setting level to %s",
                level,
            )
        level = Sudo.levels.get(level, logging.DEBUG)
        self.bot.log.setLevel(level)
        await self.bot.embed_response(ctx, f"Set log level to {level//10}")
