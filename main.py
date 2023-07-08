import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
from google.cloud import texttospeech
from player_attribute import PlayerAttribute
from player import Player
import threading


background = """
The players are all members of a mercenary company called the Silver Blades. 
They have been hired by a local lord to investigate a series of disappearances in the nearby village of Willow Creek. 
The lord believes that the disappearances are the work of goblins, and he has asked the Silver Blades to track down the goblins and bring them to justice.
"""

james = Player(
    "James",
    "human",
    "fighter",
    PlayerAttribute(10, 10, 10, 10, 10, 10),
    "An unknown fighter from a rural village named Vancouver",
)
alan = Player(
    "Alan",
    "vampire",
    "archer",
    PlayerAttribute(10, 10, 10, 10, 10, 10),
    "An well known vampire from a royal family named Seattle",
)
jj = Player(
    "JJ",
    "half elf",
    "cleric",
    PlayerAttribute(10, 10, 10, 10, 10, 10),
    "A held elf, embarking on a divine quest to heal the world and bring unity through their unique heritage and unwavering faith.",
)

count = 0


def speak_content(content: str, name):
    count = 0
    pt = 0
    while pt < len(content):
        if pt + 800 < len(content):
            end = content.rfind(".", pt, pt + 800)
            curr_content = content[pt:end]
            pt = end + 1
        else:
            curr_content = content[pt:]
            pt = len(content)

        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.SynthesisInput(text=curr_content)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-M",
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=0.75
        )

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        count += 1
        with open(f"output_{name}_{count}.mp3", "wb") as out:
            out.write(response.audio_content)
            # print(f'Audio content written to file "output_{name}_{count}.mp3"')


def initAI():
    vertexai.init(project="dnd-storytelling-game", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    text_model = TextGenerationModel.from_pretrained("text-bison@001")
    return chat_model, text_model


def init_story(temperature, text_model, keywords, players):
    storyline = ""
    format_error = True
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 500,
        "top_p": 0.8,
        "top_k": 40,
    }
    while format_error:
        storyline = text_model.predict(
            f"""
            This is a D&D Style Story Telling Game. Do not use you or I as pronouns.
            Generate an adventure with the following keywords and adventurers:
            keywords:{keywords}
            adventurers: {[player.to_string() for player in players]}
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
    worldsetting = storyline.split("<world-setting>")[1].split("</world-setting>")[0]
    cause = storyline.split("<cause>")[1].split("</cause>")[0]
    objective = storyline.split("<objective>")[1].split("</objective>")[0]
    return worldsetting, cause, objective


def generatePlayer(players):
    mode = "speech"
    # mode = "text"
    # if mode == "speech":


def main():
    chat_model, text_model = initAI()
    players = [james, alan, jj]
    worldsetting, cause, objective = init_story(
        1.0, text_model, ["goblin", "Forgotten Realms", "dragon"], players
    )
    print(f"{worldsetting}\n\n{cause}\n\n{objective}\n\n")
    t1 = threading.Thread(target=speak_content, args=(worldsetting, "worldsetting"))
    t2 = threading.Thread(target=speak_content, args=(cause, "cause"))
    t3 = threading.Thread(target=speak_content, args=(objective, "objective"))
    t1.start()
    t2.start()
    t3.start()
    parameters = {
        "temperature": 1,
        "max_output_tokens": 500,
        "top_p": 0.8,
        "top_k": 40,
    }
    examples = [
        InputOutputTextPair(
            input_text="""take the broken sword and kill the monsters""",
            output_text="""Monsters are down, now...""",
        )
    ]
    chat = chat_model.start_chat(
        context=f"""
        This is a D&D Style Story Telling Game. Do not use you or I as pronouns.
        Worldsetting:{worldsetting}
        Cause: {cause}
        Objective: {objective}
        Adventurers: {[player.to_string() for player in players]}

        While describing conversation, use format [name:"content"].
        While describing a new character that is not an adventurers (aka NPC), you should give the character a name and explain its background.
        """
    )
    response = chat.send_message(
        """
        First generate an story opening to the adventure. Explain why and how the adventurers meet together to form a party,
        Start the opening with <opening> and end with </opening>
        Then provide explanation to the terms in the previous text. Terms means NPC, location, organization, equipment.
        Start the terms with <term> and end with </term>
        """,
        **parameters,
    )
    print(f"Response from Model: {response.text}")
    t1.join()
    t2.join()
    t3.join()
    while True:
        user_input = input("Enter something: ")
        response = chat.send_message(
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
        print(f"Response from Model: {response.text}")


if __name__ == "__main__":
    main()
