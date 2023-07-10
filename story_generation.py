import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
import os

GOOGLE_CLOUD_PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT_ID"]


class Generator:
    def __init__(self, players):
        vertexai.init(project=GOOGLE_CLOUD_PROJECT_ID, location="us-central1")
        self.chat_model = ChatModel.from_pretrained("chat-bison@001")
        self.text_model = TextGenerationModel.from_pretrained("text-bison@001")
        self.worldsetting = ""
        self.cause = ""
        self.objective = ""
        self.players = players
        self.session = None

    def init_story_background(self, temperature, keywords):
        storyline = ""
        format_error = True
        parameters = {
            "temperature": temperature,
            "max_output_tokens": 512,
            "top_p": 0.8,
            "top_k": 40,
        }
        while format_error:
            storyline = self.text_model.predict(
                f"""
                This is a D&D Style Story Telling Game. Do not use you or I as pronouns.
                Generate an adventure with the following keywords and adventurers:
                keywords:{keywords}
                adventurers: {[player.to_string() for player in self.players]}
                First, provide a overview background description for the adventure, including the map, the social background, the world setting.
                Start the background with <world-setting> and end with </world-setting>
                Then, provide a cause of an adventure. The cause should explain why the adventure is related to the adventurers. Start with <cause> and end with </cause>
                In the end, provide an objective for the adventurers. Start with <objective> and end with </objective>
                """,
                **parameters,
            ).text
            format_error = (
                storyline.find("<world-setting>") == -1
                or storyline.find("</world-setting>") == -1
                or storyline.find("<cause>") == -1
                or storyline.find("</cause>") == -1
                or storyline.find("<objective>") == -1
                or storyline.find("</objective>") == -1
            )
        self.worldsetting = storyline.split("<world-setting>")[1].split(
            "</world-setting>"
        )[0]
        self.cause = storyline.split("<cause>")[1].split("</cause>")[0]
        self.objective = storyline.split("<objective>")[1].split("</objective>")[0]

    def generate_opening(self, temperature):
        parameters = {
            "temperature": temperature,
            "max_output_tokens": 500,
            "top_p": 0.8,
            "top_k": 40,
        }
        self.session = self.chat_model.start_chat(
            context=f"""
            This is a D&D Style Story Telling Game. Do not use you or I as pronouns.
            Worldsetting:{self.worldsetting}
            Cause: {self.cause}
            Objective: {self.objective}
            Adventurers: {[player.to_string() for player in self.players]}

            While describing conversation, use format [name:"content"].
            While describing a new character that is not an adventurers (aka NPC), you should give the character a name and explain its background.
            """
        )
        response = self.session.send_message(
            """
            First generate an story opening to the adventure. Explain why and how the adventurers meet together to form a party,
            Start the opening with <opening> and end with </opening>
            Then provide explanation to the terms in the previous text. Terms means NPC, location, organization, equipment.
            Start the terms with <term> and end with </term>
            """,
            **parameters,
        )
        return response

    def progress(self, temperature, user_input):
        parameters = {
            "temperature": temperature,
            "max_output_tokens": 500,
            "top_p": 0.8,
            "top_k": 40,
        }
        response = self.session.send_message(
            f"""
                {user_input}
                According to the what the adventurers say or act, generate the consequence of the action (such as NPC's reaction, or move to a new location) and slightly progress the story. 
                You should not generate the adventurers' behaviours. 
                If the adventures meet a new character, provide detailed description from what the adventurers observe.
                If the adventures move to a new location, provide detailed environment description.
                Start the opening with <story> and end with </story>
                Then provide explanation to the terms in the previous text with more details. Terms means NPC, location, organization, equipment.
                Start the terms with <term> and end with </term>
                """,
            **parameters,
        )
        return response
    
    def generate_keywords(self, text):
        parameters = {
            "temperature": 1,
            "max_output_tokens": 100,
            "top_p": 0.8,
            "top_k": 40,
        }
        response = self.text_model.predict(
            f"""
                {text}
                According to the what the text says, select a scene you believe as most important and make the summary of the scene. 
                Then, if it's possible, generate the keywords or key phrases of the summary on the following types:
                main characters, interation, other character, location/surrounding , equipment of character, other object.
                Start to prints the terms with <keyword> and end with </keyword>.
                For example, the prints should be like this: 
                <main characters> Alan, the heroes </main characters>
                <interaction> fight </interaction>
                <other characters> bandits </other characters>
                <location/surrounding> cave </location/surrounding>
                <equipment of character> swords, axes </equipment of character>
                <other object> fire </other object>
                
                """,
            **parameters,
        )
        return response
