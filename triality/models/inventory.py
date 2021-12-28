import typing as t
from dataclasses import dataclass, field

from .base import Model

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class Inventory(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    items: t.Dict[str, int] = field(default_factory=dict)
