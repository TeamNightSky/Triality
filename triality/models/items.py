import typing as t
from dataclasses import dataclass, field

from ..const import RARITY_TABLE
from .base import Model
from .farming import HarvestItems

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class GeneralSettings(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    unlock_area: t.Optional[str] = None
    spawnable: bool = True


@dataclass()
class WeaponSettings(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    weapon: bool = False
    damage: t.Optional[int] = None


@dataclass()
class FarmingSettings(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    plantable: bool = False
    grow_time: t.Optional[int] = None
    harvest_items: t.Optional[HarvestItems] = None
    needs_water_every: t.Optional[int] = None


@dataclass()
class ItemSettings(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    general: GeneralSettings = GeneralSettings()
    weapon: WeaponSettings = WeaponSettings()
    farming: FarmingSettings = FarmingSettings()


@dataclass()
class Item(Model):
    _db: "StorageClient" = field(init=False, repr=False)
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
