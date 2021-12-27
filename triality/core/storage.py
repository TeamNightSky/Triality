import os
import typing as t
from os.path import join

from postgrest_py import AsyncPostgrestClient  # type: ignore[import]

from ..models.items import Item

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
            raise ValueError("Missing url or key")
        self.bot.log.info("Created supabase client")

    async def all_items(self) -> t.List[Item]:
        data, content = await self.db.from_("Items").select("*").execute()
        return [Item(**item) for item in data]

    def _headers(self):
        return {"Authorization": f"Bearer {self.key}", "apiKey": self.key}
