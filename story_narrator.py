import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
import json
from story_world import World
import story_generator_prompts as prompts


default_parameters = {
    "temperature": 1.0,
    "max_output_tokens": 1024,
    "top_p": 0.8,
    "top_k": 40,
}


class Background:
    def __init__(self, json):
        self.position = json["position"]
        self.before = json["before-adventure"]
        self.why = json["why"]
        self.problem = json["problem"]

    def to_string(self):
        return """{
            "position": %s
            "before-adventure": %s
            "why": %s
            "problem": %s
        }""" % (
            self.position,
            self.before,
            self.why,
            self.problem,
        )

    def to_narrative(self):
        return """
        %s.
        %s.
        %s
        }""" % (
            self.before,
            self.why,
            self.problem,
        )


class Narrator:
    def __init__(self, players):
        self.chat_model = ChatModel.from_pretrained("chat-bison@001")
        self.text_model = TextGenerationModel.from_pretrained("text-bison@001")
        self.players = players
        self.world = World()
        self.background = None
        self.session = None

    def generate_world(self, keywords):
        self.world.generate_world(keywords)

    def generate_background_story(self):
        response = self.text_model.predict(
            prompts.prompt_background(
                self.world.worldsetting.to_string(),
                self.get_players(),
                self.world.worldregion.to_string(),
            ),
            **default_parameters,
        )
        self.background = Background(json.loads(response.text))

    def start_adventure(self):
        self.session = self.chat_model.start_chat(
            context=f"""
            You are a dungeon master of a role-playing game.
            Write in the third person.
            If you believe that the game reaches its end, write \"END\".

            Write the influence of the user\'s decision. 
            Write a begining of encounter. 
            Provide some suggestions on what the user can decide.

            Additional Requirements:
            Provide environment depictions at the beginning.
            Use beautiful language, word choice, and complex sentences.
            Use the tone of the novel.
            You should not make decision for me.
            You should not end the game within 5 replies.
            
            Worldsetting:{self.world.worldsetting.to_string()}
            Map: {self.world.worldregion.to_string()}
            Adventurers: {self.get_players()}
            """,
            examples=prompts.narrator_example(),
        )
        response = self.session.send_message(
            f"""
            Decision: Start
            Additional Information: {self.background.to_string()}
            """,
            **default_parameters,
        )
        return response

    def next(self, input, additional):
        response = self.session.send_message(
            f"""
            Decision: {input}
            Additional Information: {additional}
            """,
            **default_parameters,
        )
        return response

    def get_players(self):
        rv = ""
        for player in self.players:
            rv += player.to_string() + "\n"
        return rv
