"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import os
import typing as t
from os.path import join

import discord
from postgrest_py import (  # type: ignore[import]
    AsyncPostgrestClient,
    AsyncQueryRequestBuilder,
)

from triality.errors import DatabaseError
from triality.models.items import Item
from triality.models.money import Rank
from triality.models.user import User

if t.TYPE_CHECKING:
    from triality.core.bot import Triality


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

    async def get_all_plants(self) -> t.List[Item]:
        items = await self.get_all_items()
        return list(filter(lambda item: item.settings.farming.plantable, items))

    async def get_buyable_items(self) -> t.List[Item]:
        items = await self.get_all_items()
        return list(filter(lambda item: item.settings.market.buyable, items))

    async def get_all_items(self) -> t.List[Item]:
        query = self.db.from_("Items").select("*")
        data = await self.request(query)
        return [Item(**item) for item in data]

    async def update_item(self, item: Item) -> None:
        query = self.db.from_("Items").eq(slug=item.slug).upsert(item.to_json())
        await self.request(query)

    async def get_item(self, **kwargs) -> t.Optional[Item]:
        data, *_ = await self.get_from_table("Items", ["*"], **kwargs)
        if data is not None:
            return Item(**data)
        return None

    async def create_user(self, user: User) -> User:
        json = user.to_json()
        query = self.db.from_("Users").upsert(json)
        data, *_ = await self.request(query)
        self.bot.log.info(
            "Registered user %s with id %s", user.name, str(user.snowflake)
        )
        return User(**data)

    async def get_user(self, user: discord.User, created=True) -> User:
        res = {}
        try:
            res, *_ = await self.get_from_table(
                "Users", ["*"], name=user.name, snowflake=str(user.id)
            )
        except ValueError:
            res = {"name": user.name, "snowflake": user.id}
            created = False
        finally:
            db_user = User(**res)
            if not created:
                await self.create_user(db_user)
        return db_user

    async def get_all_users(self) -> t.List[User]:
        res = await self.get_from_table("Users", ["*"])
        return [User(**data) for data in res]

    async def get_from_table(
        self, table: str, cols: t.Iterable[str], **kwargs
    ) -> t.List[t.Dict[str, t.Any]]:
        query = self.db.from_(table).select(*cols)
        for field, value in kwargs.items():
            query = query.eq(field, value)
        return await self.request(query)

    async def request(
        self, query: AsyncQueryRequestBuilder
    ) -> t.List[t.Dict[str, t.Any]]:
        data, count = await query.execute()
        self.bot.log.debug(data)
        for item in data:
            if item.get("message"):
                raise DatabaseError(data.get("message"))
        return data

    async def get_ranks(self) -> t.List[Rank]:
        query = self.db.from_("Ranks").select("*")
        ranks = await self.request(query)
        return [Rank(**data) for data in ranks]

    def _headers(self):
        return {"Authorization": f"Bearer {self.key}", "apiKey": self.key}
