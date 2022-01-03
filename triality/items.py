"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import typing as t
from dataclasses import dataclass

from triality.const import RARITY_TABLE

from .base import Model

if t.TYPE_CHECKING:
    from triality.core.storage import StorageClient


@dataclass()
class GeneralSettings(Model):
    unlock_area: t.Optional[str] = None
    spawnable: bool = True


@dataclass()
class WeaponSettings(Model):
    weapon: bool = False
    damage: t.Optional[int] = None


@dataclass()
class FarmingSettings(Model):
    plantable: bool = False
    grow_time: t.Optional[int] = None
    harvest_items: t.Optional[t.Dict[str, int]] = None


@dataclass()
class MarketSettings(Model):
    buyable: bool = True


@dataclass()
class ItemSettings(Model):
    general: GeneralSettings = GeneralSettings()
    weapon: WeaponSettings = WeaponSettings()
    farming: FarmingSettings = FarmingSettings()
    market: MarketSettings = MarketSettings()


@dataclass()
class Item(Model):
    name: str
    slug: str
    description: str
    rarity: int
    cost: t.Optional[int] = None
    settings: ItemSettings = ItemSettings()
    crafting_recipe: t.Optional[t.Dict[str, int]] = None
    brewing_recipe: t.Optional[t.Dict[str, int]] = None

    @property
    def rarity_string(self):
        for string, (lower_bound, upper_bound) in RARITY_TABLE.items():
            if lower_bound <= self.rarity <= upper_bound:
                return string
        return "UNKNOWN"

    @property
    def craftable(self):
        return self.crafting_recipe is not None

    @property
    def brewable(self):
        return self.brewing_recipe is not None

    @property
    def buyable(self):
        return self.cost is not None

    async def sync_changes(self, storage: "StorageClient") -> None:
        query = storage.db.from_("Items").update(self.to_json()).eq("slug", self.slug)
        await storage.request(query)
