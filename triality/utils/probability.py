import math
import random

from triality.const import RANDOM_WEIGHT_ACCURACY


def steal_probability(user_coins: int, target_coins: int) -> float:
    return 1 / ((user_coins / (target_coins / 2 + 1)) ** 2 + 1)


def steal_percentage(user_coins: int, target_coins: int) -> float:
    if user_coins > 2 * target_coins:
        return 0
    return math.cos(math.pi * user_coins / (4 * target_coins))


def weighted_random_bool(weight: float) -> bool:
    choices = (True, False)
    weights = (weight * RANDOM_WEIGHT_ACCURACY, (1 - weight) * RANDOM_WEIGHT_ACCURACY)
    choice, *_ = random.choices(choices, weights=weights)
    return choice
