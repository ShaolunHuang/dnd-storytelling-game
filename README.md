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
https://cloud.google.com/sdk/docs/install).

```bash
gcloud auth application-default login
```

On Google Cloud Console, please enable the following APIs:
1. Vertex AI API
2. Cloud Text-to-Speech API
3. Cloud Speech-to-Text API

Provide the following environment variables:
1. STABLE_DIFFUSION_API_KEY: API key for [Stable Diffusion API](https://stablediffusionapi.com/settings/api)
2. GOOGLE_CLOUD_PROJECT_ID: Google Cloud Project ID

## Usage

```bash
python gui.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
