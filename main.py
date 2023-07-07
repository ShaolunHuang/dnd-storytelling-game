import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair


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


if __name__ == "__main__":
    main()
