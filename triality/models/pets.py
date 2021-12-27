import typing as t
from dataclasses import dataclass, field

from .base import Model


@dataclass()
class Pet(Model):
    display_name: str
    type_id: int
    svg_id: int
    color: t.Tuple[int]

    # last_fed?


@dataclass()
class PetHouse(Model):
    pets: t.List[Pet] = field(default_factory=list)
    max_pets: int = 3
