import typing as t
from dataclasses import dataclass

from .base import Model
from .farming import HarvestItems


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
    harvest_items: t.Optional[HarvestItems] = None
    needs_water_every: t.Optional[int] = None


@dataclass()
class ItemSettings(Model):
    general: GeneralSettings = GeneralSettings()
    weapon: WeaponSettings = WeaponSettings()
    farming: FarmingSettings = FarmingSettings()


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
        pass

    @property
    def craftable(self):
        return self.crafting_recipe is not None

    @property
    def brewable(self):
        return self.brewing_recipe is not None

    @property
    def buyable(self):
        return self.cost is not None
