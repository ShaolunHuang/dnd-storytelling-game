from player_attribute import PlayerAttribute
from player_attribute import PlayerInventory
import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
from google.cloud import texttospeech


class Character:
    def create(
        self,
        name,
        sex,
        age,
        race,
        level,
        player_class,
        attributes,
        inventory,
        background,
    ):
        self.name = name
        self.sex = sex
        self.background = background
        self.attributes = attributes
        self.race = race
        self.age = age
        self.level = level
        self.inventory = inventory
        self.c_class = player_class
        self.generated = True

    def init_from_json(self, json):
        self.name = json["name"]
        self.sex = json["sex"]
        self.background = json["description"]
        self.attributes = PlayerAttribute(json["attributes"])
        self.race = json["race"]
        self.age = json["age"]
        self.level = json["level"]
        self.inventory = PlayerInventory(json["equipment"])
        self.c_class = json["class"]
        self.generated = True

    def prepare(self, name, inhabitant):
        self.name = name
        self.inhabitant = inhabitant
        self.generated = False

    def __init__(self):
        self.generated = False

    def to_string(self):
        return """{
            "name":%s,
            "description":%s,
            "sex":%s,
            "age":%s,
            "level":%s,
            "class":%s,
            "race":%s,
            "attributes":%s,
            "equipment":%s,
            "relationship":%s
        }
        """ % (
            self.name,
            self.background,
            self.sex,
            self.age,
            self.level,
            self.c_class,
            self.race,
            self.attributes.to_string(),
            self.inventory.to_string(),
            "",
        )


def generatePlayer(mode):
    # mode = "speech"
    # mode = "text"
    if mode == "speech":
        # call speech to text
        input = "Please enter the name of the player"
    else:
        input = input(
            "Select the way to generate player: A. Description; B. Fill in the blank; C. Randomly generate"
        )
        if input.upper() == "A":
            input = input(
                "Please enter the following information: name, sex, age, race, level, player_class, attributes, background"
            )
