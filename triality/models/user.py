import typing as t
from dataclasses import dataclass, field

from .base import Model
from .brewing import Brewery
from .farming import Farm
from .inventory import Inventory
from .money import Money
from .pets import PetHouse
from .xp import XPTable

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class User(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    snowflake: int  # This is the discord user id field
    # name: str = "UNKOWN"
    name: str  # Required parameter (this is the users discord name)
    money: Money = Money()
    inventory: Inventory = Inventory()
    xp: XPTable = XPTable()
    farm: Farm = Farm()
    brewery: Brewery = Brewery()
    pets: PetHouse = PetHouse()

    async def sync_changes(self):
        data, _ = (
            await self._db.from_("Users")
            .eq("snowflake", self.snowflake)
            .update(self.to_json())
            .execute()
        )
