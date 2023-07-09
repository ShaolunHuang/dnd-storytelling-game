import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)
from google.cloud import texttospeech
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from player_attribute import PlayerAttribute, PlayerInventory
from player import Character
from image_generator import ImageGenerator
import os
import threading
from story_generation import Generator
from story_narrator import Narrator

background = """
The players are all members of a mercenary company called the Silver Blades. 
They have been hired by a local lord to investigate a series of disappearances in the nearby village of Willow Creek. 
The lord believes that the disappearances are the work of goblins, and he has asked the Silver Blades to track down the goblins and bring them to justice.
"""

james = Character()
james.create(
    "James",
    "Male",
    20,
    "human",
    10,
    "fighter",
    PlayerAttribute(10, 10, 10, 10, 10, 10),
    PlayerInventory([], [], [], [], [], [], []),
    "An unknown fighter from a rural village named Vancouver",
)
alan = Character()
alan.create(
    "Alan",
    "Male",
    20,
    "vampire",
    10,
    "archer",
    PlayerAttribute(10, 10, 10, 10, 10, 10),
    PlayerInventory([], [], [], [], [], [], []),
    "A well known vampire from a royal family named Seattle",
)
jj = Character()
jj.create(
    "JJ",
    "Male",
    20,
    "half-elf",
    10,
    "cleric",
    PlayerAttribute(10, 10, 10, 10, 10, 10),
    PlayerInventory([], [], [], [], [], [], []),
    "A half-elf, embarking on a divine quest to heal the world and bring unity through their unique heritage and "
    "unwavering faith.",
)

GOOGLE_CLOUD_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
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
        with open(f"resources/audios/output_{name}_{count}.mp3", "wb") as out:
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
        recognizer=f"projects/{GOOGLE_CLOUD_PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


def main(players, keywords):
    vertexai.init(project=GOOGLE_CLOUD_PROJECT_ID, location="us-central1")
    narrater = Narrator(players)
    narrater.generate_world(keywords)
    image_gen = ImageGenerator()
    image_gen.get_image(", ".join(keywords))
    print(
        f"{narrater.world.worldsetting.to_narrative()}\n\n{narrater.world.worldregion.to_narrative()}\n\n"
    )
    text_to_speech(narrater.world.worldsetting.to_narrative(), "worldsetting")
    text_to_speech(narrater.world.worldregion.to_narrative(), "region")

    narrater.generate_background_story()
    print(
        f"Position: {narrater.background.position} \n\n{narrater.background.to_narrative()}\n\n"
    )
    text_to_speech(narrater.background.to_narrative(), "background")

    response = narrater.start_adventure()
    print(f"{response.text}\n")
    text_to_speech(response.text, "story")
    while True:
        user_input = input("")
        response = narrater.next(user_input, "")
        text_to_speech(response.text, "story")
        print(f"{response.text}\n")


if __name__ == "__main__":
    main([james, alan, jj], ["Cyberpunk", "desert", "city", "lava"])
