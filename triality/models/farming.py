import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from .base import Model

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class HarvestItems(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    guaranteed: t.Dict[str, int] = field(default_factory=dict)
    random: t.Dict[str, int] = field(default_factory=dict)


@dataclass()
class Crop(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    planted_seed: str
    end: datetime
    last_watered: datetime


@dataclass()
class Farm(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    in_progress: t.List[Crop] = field(default_factory=list)
    max_in_progress: int = 10
