"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

INTEREST_RATE = 0.01
INTEREST_WAIT = 1800

OWNER_ID = 301055957734129665

ADMINS = (515854207837011970,)

DEV_SERVERS = [798004434021384264]

DESCRIPTION = ""
MAX_MESSAGES = 2000
RANDOM_WEIGHT_ACCURACY = 10 ** 5
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%i.%f"

EXTENSIONS = [
    "triality.core.cogs.basic.items",
    "triality.core.cogs.basic.money",
    "triality.core.cogs.basic.farm",
    "triality.core.cogs.error",
    "triality.core.cogs.sudo",
]

RARITY_TABLE = {
    "MYTHIC": (0, 5),
    "LEGENDARY": (6, 1),
    "EPIC": (11, 40),
    "RARE": (41, 80),
    "UNCOMMON": (81, 140),
    "COMMON": (141, 10000),
}
XP_SCALE = 1.5


FAVOR_MESSAGES = [
    "You shuffle some cards for your boss and they pay you $%i for it.",
    "You help an old woman across the street. She gives you $%i in thanks.",
    "You got in a car crash, doing your enemy a favor. In thanks, they give you $%i",
    "You saved someone from slipping on a banana peel. They gave you $%i",
    "You got a cat down from a tree. You are rewarded with $%i",
    "You saved a goldfish on the street; their owner gives you $%i",
    "You help move some furniture, and ware given $%i",
    "You helped a travelling wombat protect their wombat belongings. They scrounge up $%i for you.",
    "You budged to the front of the line, and someone gives you $%i because you let them keep their spot.",
    "You are such a suck-up to your coworkers that you wash everyone's toilets before they sit on them. Your boss doesn't like it all that much. But pays you $%i anyway.",
]

WORK_MESSAGES = [
    "You go to work and help some frustrating clients.",
    "You made some computational forms.",
    "You pogo stick-ed across some stepping stones.",
    "You cleaned the airplane toilets.",
    "You mixed chemicals in the name of science.",
    "You went to McDonalds to be a ketchup mascot.",
    "You put horse shoes on horse feet.",
    "You dumped crap into the atmosphere.",
    "You pulled up hydrocarbons from the ground.",
    "You coded a discord bot.",
    "You yelled at your inferiors telling them to keep on working.",
    "You suffered through a day babysitting toddlers.",
    'You made the roads "better".',
    "You art-ed a painting.",
    "You swam across the atlantic ocean.",
]

PROMOTED_MESSAGES = [
    "Your boss is impressed and gave you a raise.",
    "You bribe your supervisor to bribe your boss to give you a raise.",
    'Your boss died and said "I will (dying sounds) let you have a promotion" as their last words.',
    "Your boss wanted you out of the office so bad that they promoted you.",
    'You told your boss that they are "The best boss in the entire world", so they gave you a promotion.',
    "Your boss falls off a building, and lands into your arms while you were running away. They gave you a promotion.",
    "Your boss sees you punching their least favorite worker, and gives you a promotion.",
]

STEAL_FAIL_MESSAGES = [
    "You practically suck as thievery.",
    "You kicked the cat, alerting your target.",
    "A (not so) dear friend sold you out.",
    "You slipped and fell on a banana peel.",
    "You shouldn't steal from a cop.",
    "Your party gun went off during the theft.",
]

STEAL_SUCCESS_MESSAGES = [
    "YOU ACTUALLY MANAGED TO PULL THE HEIST OFF.",
    "Your target was in a coma, and didn't see you.",
    "You stole candy from a baby. Good job!",
    "You fought a brave and honorable battle.",
    "Your target forgot their valuables outside.",
]

EMPTY_STEAL_MESSAGES = [
    "You tried to rob them but there was nothing to steal.",
    "How dare you rob a poor person! They had nothing for you.",
    "You were a coward and got nothing.",
    "You fell off a balcony and failed to grab anything.",
    "Your target thought you were their grandma, and let you get away.",
]

GIVE_MESSAGES = [
    "You are in a giving mood and decide to give money to complete strangers.",
    "It's your nephew's birthday so you buy him a gift card.",
    "You drop money on the ground and someone picks it up.",
    "You felt that someone was in need, so you gave your money to someone else.",
    "You do an old western-style standoff, and then give the other person your money.",
]

HELP_MESSAGES = [
    "The help you requested!",
    "Really you want help? Ok.",
    "Sure glad to help.",
    "Help has arrived!",
]

HELP_MESSAGES = [
    msg + " (Psst. Use `help {command}` to see more!)" for msg in HELP_MESSAGES
]
