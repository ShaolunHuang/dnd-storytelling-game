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
        return f"strength: {self.strength},constitution: {self.constitution},dexterity: {self.dexterity},intelligence: {self.intelligence},wisdom: {self.wisdom},charisma: {self.charisma}"
