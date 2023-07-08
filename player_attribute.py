import json


class PlayerAttribute:
    def __init__(
        self, strength, constitution, dexterity, intelligence, wisdom, charisma
    ) -> None:
        self.strength = strength
        self.constitution = constitution
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    def to_string(self):
        return """{
            "strength":%d,
            "constitution":%d,
            "dexterity":%d,
            "intelligence":%d,
            "wisdom":%d,
            "charisma":%d
            }""" % (
            self.strength,
            self.constitution,
            self.dexterity,
            self.intelligence,
            self.wisdom,
            self.charisma,
        )


class PlayerInventory:
    def __init__(
        self, helmet, chestplate, leggings, boots, righthand, lefthand, inventory
    ) -> None:
        self.inventory = inventory
        self.helmet = helmet
        self.chestplate = chestplate
        self.leggings = leggings
        self.boots = boots
        self.righthand = righthand
        self.lefthand = lefthand

    def __init__(self, json) -> None:
        self.inventory = json["inventory"]
        self.helmet = json["helmet"]
        self.chestplate = json["chestplate"]
        self.leggings = json["leggings"]
        self.boots = json["boots"]
        self.righthand = json["right-hand"]
        self.lefthand = json["left-hand"]

    def to_string(self):
        return """{
            "helmet":%s,
            "chestplate":%s,
            "leggings":%s,
            "boots":%s,
            "righthand":%s,
            "lefthand":%s,
            "inventory":%s
            }""" % (
            json.dumps(self.helmet),
            json.dumps(self.chestplate),
            json.dumps(self.leggings),
            json.dumps(self.boots),
            json.dumps(self.righthand),
            json.dumps(self.lefthand),
            json.dumps(self.inventory),
        )
