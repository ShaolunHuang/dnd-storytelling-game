import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
from google.cloud import texttospeech
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from player_attribute import PlayerAttribute
from player import Player
import threading
from story_generation import Generator


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
    "half-elf",
    "cleric",
    PlayerAttribute(10, 10, 10, 10, 10, 10),
    "A half-elf, embarking on a divine quest to heal the world and bring unity through their unique heritage and unwavering faith.",
)

TOKEN_SIZE = 800


def text_to_speech(content: str, name):
    count = 0
    pt = 0
    while pt < len(content):
        if pt + TOKEN_SIZE < len(content):
            end = content.rfind(".", pt, pt + TOKEN_SIZE)
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
            print(f'Audio content written to file "output_{name}_{count}.mp3"')


def speech_to_text(audio):
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio, "rb") as f:
        content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config={}, language_codes=["en-US"], model="latest_long"
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/dnd-storytelling-game/locations/global/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


def main():
    generator = Generator()
    players = [james, alan, jj]
    worldsetting, cause, objective = generator.init_story_background(
        1.0, ["goblin", "Forgotten Realms", "dragon"], players
    )
    print(f"{worldsetting}\n\n{cause}\n\n{objective}\n\n")
    text_to_speech(worldsetting, "worldsetting")
    text_to_speech(cause, "cause")
    text_to_speech(objective, "objective")

    examples = [
        InputOutputTextPair(
            input_text="""take the broken sword and kill the monsters""",
            output_text="""Monsters are down, now...""",
        )
    ]
    response = generator.generate_opening(1.0)
    print(f"Response from Model: {response.text}")
    while True:
        user_input = input("Enter something: ")
        response = generator.progress(1.0, user_input)
        print(f"Response from Model: {response.text}")


if __name__ == "__main__":
    main()
