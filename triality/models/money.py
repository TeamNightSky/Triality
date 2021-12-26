from dataclasses import dataclass

from .base import Model


@dataclass()
class Bank(Model):
    coins: int


@dataclass()
class Purse(Model):
    coins: int


@dataclass()
class Money(Model):
    bank: Bank
    purse: Bank
