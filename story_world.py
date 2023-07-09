import json
import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
import story_generator_prompts as prompts
from player import Character


class World:
    def __init__(self):
        self.chat_model = ChatModel.from_pretrained("chat-bison@001")
        self.text_model = TextGenerationModel.from_pretrained("text-bison@001")
        self.worldsetting = None
        self.worldregion = None
        self.regions = {}
        self.structures = {}
        self.npcs = {}

    def generate_world(self, keywords):
        parameters = {
            "temperature": 1.0,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40,
        }
        worldsetting_string = self.text_model.predict(
            prompts.prompt_worldsetting(keywords),
            **parameters,
        ).text
        self.worldsetting = Worldsetting(json.loads(worldsetting_string))

        worldregion = self.text_model.predict(
            prompts.prompt_region(
                context=self.worldsetting,
                size="large",
                name=self.worldsetting.name,
            ),
            **parameters,
        ).text
        self.worldregion = Region()
        self.worldregion.init_from_json(json.loads(worldregion))
        for subregion in self.worldregion.subregions:
            if not subregion in self.regions:
                self.regions[subregion] = Region()
                self.regions[subregion].prepare(subregion, self.worldregion)

    def generate_region(self, site_name, parent_site):
        parameters = {
            "temperature": 1.0,
            "max_output_tokens": 512,
            "top_p": 0.8,
            "top_k": 40,
        }
        response = json.loads(
            self.text_model.predict(
                prompts.prompt_region(
                    context=self.worldsetting,
                    name=site_name,
                    parent_region=json.dumps(parent_site),
                ),
                **parameters,
            )
        )
        generated_region = Region()
        generated_region.init_from_json(response)
        for subregion in generated_region.subregions:
            if not subregion in self.regions:
                self.regions[subregion] = Region()
                self.regions[subregion].prepare(subregion, self.worldregion)
        self.regions[generated_region.name] = generated_region

    def generate_structure(self, site_name, parent_site):
        parameters = {
            "temperature": 1.0,
            "max_output_tokens": 512,
            "top_p": 0.8,
            "top_k": 40,
        }
        generated_structure = Structure()
        generated_structure.init_from_json(
            json.loads(
                self.text_model.predict(
                    prompts.prompt_structure(
                        self.worldsetting, site_name, json.dumps(parent_site)
                    ),
                    **parameters,
                )
            )
        )
        for npc in generated_structure.npcs:
            if not npc in self.npcs:
                self.npcs[npc] = Character(npc, generated_structure)
        self.structures[generated_structure["name"]] = generated_structure

    def generate_npc(self, npc_name, parent_site):
        parameters = {
            "temperature": 1.0,
            "max_output_tokens": 512,
            "top_p": 0.8,
            "top_k": 40,
        }
        generated_npc = Character()
        generated_npc.init_from_json(
            self.text_model.predict(
                prompts.prompt_npc(npc_name, json.dumps(parent_site)),
                **parameters,
            )
        )
        self.npcs[generated_npc["name"]] = generated_npc


class Worldsetting:
    def __init__(self, json):
        self.name = json["name"]
        self.geography = json["geography"]
        self.econimic = json["economic and technology"]
        self.society = json["society"]
        self.inhabitants = json["inhabitants"]
        self.ability = json["ability-system"]
        self.lore = json["history"]

    def to_string(self):
        return """{
            "name":%s,
            "geography":%s,
            "economic and technology":%s,
            "society":%s,
            "inhabitants":%s,
            "ability-system":%s,
            "lore":%s
            }""" % (
            self.name,
            self.geography,
            self.econimic,
            self.society,
            self.inhabitants,
            self.ability,
            self.lore,
        )

    def to_narrative(self):
        return """
            %s.  
            %s  
            %s  
            %s  
            %s  
            %s  
            %s  
            """ % (
            self.name,
            self.geography,
            self.econimic,
            self.society,
            self.inhabitants,
            self.ability,
            self.lore,
        )


class Region:
    def init_from_json(self, json):
        self.name = json["name"]
        self.types = json["type"]
        self.description = json["description"]
        self.subregions = json["sub-regions"]
        self.structures = json["structures"]
        self.inhabitants = json["inhabitants"]
        self.generated = True

    def prepare(self, name, parent):
        self.name = name
        self.parent = parent
        self.generated = False

    def __init__(self):
        self.generated = False

    def to_string(self):
        return """{
            "name":%s,
            "type":%s,
            "description":%s,
            "sub-regions":%s,
            "structures":%s,
            "inhabitants":%s,
            }""" % (
            self.name,
            json.dumps(self.types),
            self.description,
            json.dumps(self.subregions),
            json.dumps(self.structures),
            json.dumps(self.inhabitants),
        )

    def to_narrative(self):
        return """
                Region Name: %s
                Region Type: %s
                Description: %s
                Sub-regions: %s
                Landmarks: %s
                inhabitants: %s
                """ % (
            self.name,
            json.dumps(self.types),
            self.description,
            json.dumps(self.subregions),
            json.dumps(self.structures),
            json.dumps(self.inhabitants),
        )


class Structure:
    def init_from_json(self, json):
        self.name = json["name"]
        self.types = json["type"]
        self.description = json["description"]
        self.npcs = json["npc"]
        self.generated = True

    def __init__(self):
        self.generated = False

    def prepare(self, name, parent):
        self.name = name
        self.parent = parent
        self.generated = False

    def to_string(self):
        return """{
            "name":%s,
            "type":%s,
            "description":%s,
            "npc":%s
            }""" % (
            self.name,
            json.dumps(self.types),
            self.description,
            json.dumps(self.sublocations),
            json.dumps(self.npcs),
        )
