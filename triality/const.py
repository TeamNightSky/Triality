INTEREST_RATE = 0.01
INTEREST_WAIT = 1800

OWNER_ID = 301055957734129665

ADMINS = (515854207837011970,)

DESCRIPTION = ""
MAX_MESSAGES = 2000

"""
"default-money": {
    "type": "monetary",
    "bank": {
        "coins": 250
    },
    "purse": {
        "coins": 50
    },
    "salary": 50
},
"default-inventory": {
    "type": "inventory",
    "items": {}
},
"default-auction": {
    "type": "auction",
    "id": null,
    "item": null,
    "owner": null,
    "bids": [],
    "end": null,
    "start-bid": null,
    "collected": [
        false,
        false
    ],
    "top_bidder": null
},
"default-xp": {
    "type": "xp",
    "xp": {
        "journeying": 0,
        "magical": 0,
        "alchemy": 0,
        "combat": 0,
        "finding": 0,
        "crafting": 0,
        "auctioning": 0,
        "intelligence": 0,
        "farming": 0
    },
    "id": null
},
"default-quests": {
    "quests": [],
    "type": "quests",
    "id": null
},
"default-farm": {
    "type": "farm",
    "id": null,
    "growing": [],
    "max-crops": 10
},
"""

RARITY_TABLE = {
    "MYTHIC": (0, 5),
    "LEGENDARY": (6, 1),
    "epic": (11, 40),
    "rare": (41, 80),
    "uncommon": (81, 140),
    "common": (141, 10000),
}
XP_SCALE = 1.5
