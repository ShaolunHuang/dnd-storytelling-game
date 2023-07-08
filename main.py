import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from google.cloud import texttospeech
import threading


def main():
    vertexai.init(project="dnd-storytelling-game", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    chat = chat_model.start_chat(
        context="""This is a D&D Style Story Telling Game. Players or Users are a group of adventurers who have been 
        hired by a local lord to investigate a series of disappearances in the nearby village. They have been warned 
        that the village is rumored to be haunted, but they are determined to find out what is really going on. You 
        in this game play as a story teller, take players\' input and give out consequences of such player action. 
        Please provide an intro after prompt \"start game\". After each generated response, please provide 2 or 3 
        encounters and add \"Please decide on your action...\"""",
        examples=[
            InputOutputTextPair(
                input_text="""take the broken sword and kill the monsters""",
                output_text="""Monsters are down, now..."""
            )
        ]
    )
    response = chat.send_message("""start game""", **parameters)
    print(f"Response from Model: {response.text}")


def main2(content, name):
    count = 0
    pt = 0
    # Split the content by last full stop before 800 characters each
    while pt < len(content):
        if pt + 800 < len(content):
            end = content.rfind('.', pt, pt + 800)
            curr_content = content[pt:end]
            pt = end + 1
        else:
            curr_content = content[pt:]
            pt = len(content)

        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.SynthesisInput(
            text=curr_content
        )

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-M",
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=0.75
        )

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        count += 1
        # The response's audio_content is binary.
        with open(f"output_{name}_{count}.mp3", "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "output_{name}_{count}.mp3"')


content = """The Forgotten Realms is a vast world full of adventure and danger. It is a land of towering mountains, 
deep forests, and endless plains. There are many different cultures and races living in the Forgotten Realms, 
including humans, elves, dwarves, and halflings.  The Forgotten Realms is also home to many different creatures, 
both good and evil. There are dragons, giants, goblins, orcs, and many others.  The adventurers are in the town of 
Phandalin, which is located in the Sword Coast region of the Forgotten Realms. Phandalin is a small town, but it is a 
thriving community. The town is ruled by a council of elders, and there is a small militia that helps to keep the peace.

The adventurers are approached by a man named Elminster, who is a powerful wizard. Elminster tells the adventurers 
that there is a group of goblins who are terrorizing the countryside. The goblins have been attacking farms and 
villages, and they have even kidnapped some children.  Elminster asks the adventurers to help him defeat the 
goblins and rescue the children. The adventurers agree to help Elminster, and they set out on their journey.

The adventurers travel to the goblin village, which is located in a nearby forest. The goblins are led by a 
powerful goblin named Gnash. Gnash is a cruel and vicious creature, and he has no mercy for his enemies.  The 
adventurers battle their way through the goblin village, and they eventually defeat Gnash. The adventurers rescue 
the children, and they return to Phandalin.  The people of Phandalin are grateful to the adventurers for their 
help, and they hold a feast in their honor. The adventurers are hailed as heroes, and they are given a large 
reward."""

if __name__ == "__main__":
    t1 = threading.Thread(target=main2, args=(content, "background"))
    t2 = threading.Thread(target=main2, args=(content, "second_background"))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

