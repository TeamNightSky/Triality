from dataclasses import dataclass

from .base import Model


@dataclass()
class Bank(Model):
    coins: int = 250


@dataclass()
class Purse(Model):
    coins: int = 50


@dataclass()
class Rank(Model):
    level: int = 0
    title: str = "PEASANT"
    salary: int = 50
    image: str = ""
    promotion_chance_increase: float = 0.05
    progress: float = 0


@dataclass()
class Money(Model):
    bank: Bank = Bank()
    purse: Purse = Purse()
    rank: Rank = Rank()
