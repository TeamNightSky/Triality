from dataclasses import dataclass

from .base import Model
from .money import Money


@dataclass()
class User(Model):
    money: Money
