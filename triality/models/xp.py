from dataclasses import dataclass

from .base import Model


@dataclass()
class XPTable(Model):
    journeying: int = 0
    magical: int = 0
    alchemy: int = 0
    combat: int = 0
    finding: int = 0
    crafting: int = 0
    auctioning: int = 0
    intelligence: int = 0
    farming: int = 0
