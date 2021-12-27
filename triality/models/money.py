from dataclasses import dataclass

from .base import Model


@dataclass()
class Bank(Model):
    coins: int = 250


@dataclass()
class Purse(Model):
    coins: int = 50


@dataclass()
class Money(Model):
    bank: Bank = Bank()
    purse: Purse = Purse()
    salary: int = 50
