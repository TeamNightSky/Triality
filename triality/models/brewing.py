import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from .base import Model

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class Potion(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    end: datetime
    ingredients: t.Dict[str, int]
    finish_item: str
    finish_xp: int


@dataclass()
class Brewery(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    in_progress: t.List[Potion] = field(default_factory=list)
    max_in_progress: int = 3
