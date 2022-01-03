"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import typing as t
from dataclasses import dataclass

from .base import Model
from .brewing import Brewery
from .farming import Farm
from .inventory import Inventory
from .money import Money
from .pets import PetHouse
from .xp import XPTable

if t.TYPE_CHECKING:
    from ..core.manager import StorageManager


@dataclass()
class User(Model):
    snowflake: int  # This is the discord user id field
    name: str  # Required parameter (this is the users discord name)
    money: Money = Money()
    inventory: Inventory = Inventory()
    xp: XPTable = XPTable()
    farm: Farm = Farm()
    brewery: Brewery = Brewery()
    pets: PetHouse = PetHouse()

    async def sync_changes(self, storage: "StorageManager"):
        query = (
            storage.db.from_("Users")
            .update(self.to_json())
            .eq("snowflake", str(self.snowflake))
        )
        await storage.request(query)
