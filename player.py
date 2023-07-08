from player_attribute import PlayerAttribute


class Player:
    def __init__(self, name, race, _class, attributes, background) -> None:
        self.name = name
        self.background = background
        self.attributes = attributes
        self.race = race
        self._class = _class

    def to_string(self):
        return f""" {self.name} (Class: {self._class}, Race: {self.race}, Attributes: [{self.attributes.to_string()}], Background: {self.background}) """
