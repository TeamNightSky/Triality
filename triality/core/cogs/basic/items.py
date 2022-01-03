from discord.commands import ApplicationContext, slash_command
from discord.ext.commands import Cog  # type: ignore[attr-defined]

from triality import const
from triality.converters import ItemConverter
from triality.core.bot import Triality


class Inventory(Cog):
    def __init__(self, bot: Triality) -> None:
        self.bot = bot

    @slash_command(guild_ids=const.DEV_SERVERS)
    async def inventory(self, ctx: ApplicationContext):
        await self.bot.embed_response(ctx, "Fetching your inventory...")
        db_user = await self.bot.storage.get_user(ctx.user)
        await self.bot.embed_response(
            ctx,
            title="Your Inventory",
            content=str(db_user.inventory.items),
            follow_up=True,
        )

    async def spawn_artifacts(self):
        pass


class Market(Cog):
    def __init__(self, bot: Triality) -> None:
        self.bot = bot

    @slash_command(guild_ids=const.DEV_SERVERS)
    async def market(self, ctx: ApplicationContext):

        await ctx.respond("Hi!")

    @slash_command(guild_ids=const.DEV_SERVERS)
    async def item(self, ctx: ApplicationContext, item: ItemConverter):
        await ctx.respond(item.to_json_string())


def setup(bot: Triality) -> None:
    bot.add_cog(Inventory(bot))
    bot.add_cog(Market(bot))
