from discord.commands import ApplicationContext
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
