import typing as t

from discord.commands import Permission, SlashCommandGroup
from discord.ext.commands import Cog, Context  # type: ignore[attr-defined]

from triality import const

if t.TYPE_CHECKING:
    from ..bot import Triality


def setup(bot: "Triality"):
    bot.add_cog(Sudo(bot))


class Sudo(Cog):
    def __init__(self, bot: "Triality"):
        self.bot = bot

    sudo_group = SlashCommandGroup(
        "sudo",
        "Admin Commands",
        permissions=[Permission(const.ADMIN_ROLE, 1, True, const.DEV_SERVER)],
    )

    @sudo_group.command(name="whoami")
    async def whoami(self, ctx: Context) -> None:
        await ctx.respond("`root`")

    @sudo_group.command(name="reload", aliases=["r", "refresh"])
    async def reload(self, ctx: Context) -> None:
        msg = await ctx.send(":arrows_counterclockwise: Reloading...")
        for ext in self.bot.extensions:
            self.bot.unload_extension(ext)
            self.bot.init_extension(ext)
        await msg.edit(":white_check_mark: Reloaded")
