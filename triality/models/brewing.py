import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from .base import Model


@dataclass()
class Potion(Model):
    end: datetime
    ingredients: t.Dict[str, int]
    finish_item: str
    finish_xp: int


@dataclass()
class Brewery(Model):
    in_progress: t.List[Potion] = field(default_factory=list)
    max_in_progress: int = 3
