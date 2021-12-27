import typing as t
from dataclasses import dataclass, field

from .base import Model


@dataclass()
class Inventory(Model):
    items: t.Dict[str, int] = field(default_factory=dict)
