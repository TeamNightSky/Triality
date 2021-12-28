import os
import typing as t
from os.path import join

import discord
from postgrest_py import AsyncPostgrestClient  # type: ignore[import]

from ..models.items import Item
from ..models.user import User

if t.TYPE_CHECKING:
    from .bot import Triality


class StorageClient:
    key: t.Optional[str] = os.getenv("SUPA_KEY")
    url: t.Optional[str] = os.getenv("SUPA_URL")

    def __init__(self, bot: "Triality"):
        self.bot = bot
        if self.url is not None and self.key is not None:
            self.db = AsyncPostgrestClient(
                base_url=join(self.url, "rest/v1"), headers=self._headers()
            )
        else:
            self.bot.log.critical("Missing postgrest url and/or key.")
            raise ValueError("Missing url or key")
        self.bot.log.info("Created supabase client")

    async def get_all_items(self) -> t.List[Item]:
        self.bot.log.warning(
            "Avoid using get_all_items -- this may be a data steal attempt"
        )
        data, _ = await self.db.from_("Items").select("*").execute()
        return [Item(**item) for item in data]

    async def update_item(self, item: Item, **kwargs) -> None:
        await self.db.from_("Items").eq(slug=item.slug).update(**kwargs)

    async def get_item(self, **kwargs) -> t.Optional[Item]:
        data = await self.get_from_table("Items", ["*"], **kwargs)
        if data is not None:
            return Item(**data)
        return None

    async def create_user(self, user: User) -> User:
        json = user.to_json()
        data, _ = await self.db.from_("Users").insert(json).execute()
        self.bot.log.debug(data)
        self.bot.log.info(
            "Registered user %s with id %s", user.name, str(user.snowflake)
        )
        return User(**data)

    async def get_user(self, user: discord.User) -> User:
        res = await self.get_from_table(
            "Users", ["*"], name=user.name, snowflake=user.id
        )
        if res is None:
            res = {}
        db_user = User(**res)
        if res is None:
            await self.create_user(db_user)
        return db_user

    async def get_from_table(
        self, table: str, cols: t.Iterable[str], **kwargs
    ) -> t.Optional[dict]:
        query = self.db.from_(table).select(*cols)
        for field, value in kwargs.items():
            query = query.eq(field, value)
        result = await query.execute()
        try:
            (data, *_), count = result
        except ValueError:
            self.bot.log.error("ValueError: " + str(result))
            return None
        return data

    def _headers(self):
        return {"Authorization": f"Bearer {self.key}", "apiKey": self.key}
