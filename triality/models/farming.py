import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from .base import Model


@dataclass()
class Crop(Model):
    planted_seed: str
    end: datetime
    last_watered: t.Optional[datetime] = None


@dataclass()
class Farm(Model):
    in_progress: t.List[Crop] = field(default_factory=list)
    max_in_progress: int = 10
