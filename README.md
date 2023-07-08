# DND StoryTelling Game

dnd-storytelling-game is a project for Google Vertex AI Hackathon. It uses AI to create a multiplayer D&D-style storytelling game with in-game user text input that influences the story with fixed and accurate combat logic.


## Installation

Please use Python 3.7 or above.

Optionally create new virtual environment for python.

```bash
python -m venv venv
source venv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies.

```bash
python -m pip install -r requirements.txt
```

Install Google CLI and authenticate with your Google account from this [url](
https://cloud.google.com/sdk/docs/install?hl=zh-cn).

```bash
gcloud auth application-default login
```

## Usage

```bash
python main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
