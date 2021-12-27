from dataclasses import dataclass

from .base import Model
from .brewing import Brewery
from .farming import Farm
from .inventory import Inventory
from .money import Money
from .pets import PetHouse
from .xp import XPTable


@dataclass()
class User(Model):
    name: str
    snowflake: int
    money: Money = Money()
    inventory: Inventory = Inventory()
    xp: XPTable = XPTable()
    farm: Farm = Farm()
    brewery: Brewery = Brewery()
    pets: PetHouse = PetHouse()
