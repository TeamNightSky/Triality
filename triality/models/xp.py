import typing as t
from dataclasses import dataclass, field

from .base import Model

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class XPTable(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    journeying: int = 0
    magical: int = 0
    alchemy: int = 0
    combat: int = 0
    finding: int = 0
    crafting: int = 0
    auctioning: int = 0
    intelligence: int = 0
    farming: int = 0
