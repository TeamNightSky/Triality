import typing as t
from dataclasses import dataclass, field

from .base import Model

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class Pet(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    display_name: str
    type_id: int
    svg_id: int
    color: t.Tuple[int]

    # last_fed?


@dataclass()
class PetHouse(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    pets: t.List[Pet] = field(default_factory=list)
    max_pets: int = 3
