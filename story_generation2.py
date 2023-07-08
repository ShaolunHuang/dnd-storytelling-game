import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
import json
import story_generator_prompts as prompts


class Location:
    def __init__(self, json):
        self.name = json["name"]
        self.types = json["type"]
        self.description = json["description"]
        self.sublocations = json["sub-locations"]
        self.npcs = json["npc"]


class Generator:
    def __init__(self, players):
        vertexai.init(project="dnd-storytelling-game", location="us-central1")
        self.chat_model = ChatModel.from_pretrained("chat-bison@001")
        self.text_model = TextGenerationModel.from_pretrained("text-bison@001")
        self.worldsetting = ""
        self.cause = ""
        self.objective = ""
        self.players = players
        self.session = None

    def generate_location(self, site_name, parent_site):
        parameters = {
            "temperature": 1.0,
            "max_output_tokens": 512,
            "top_p": 0.8,
            "top_k": 40,
        }
        response = self.text_model.predict(
            prompts.prompt_site(site_name, json.dumps(parent_site)),
            **parameters,
        )
        return Location(json.loads(response.text))

    def generate_npc(self, npc_name, parent_site):
        parameters = {
            "temperature": 1.0,
            "max_output_tokens": 512,
            "top_p": 0.8,
            "top_k": 40,
        }
        response = self.text_model.predict(
            prompts.prompt_npc(npc_name, json.dumps(parent_site)),
            **parameters,
        )
        return Location(json.loads(response.text))
