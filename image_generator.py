import requests
import json
import os


class ImageGenerator:

    def __init__(self):
        self.api_key = os.getenv("STABLE_DIFFUSION_API_KEY")

    def get_image(self, prompt):
        uri = "https://stablediffusionapi.com/api/v3/dreambooth"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "key": self.api_key,
            "model_id": "anything-v5",
            "prompt": prompt,
            "negative_prompt": "",
            "width": "512",
            "height": "512",
            "samples": "1",
            "num_inference_steps": "30",
            "safety_checker": "no",
            "enhance_prompt": "no",
            "seed": None,
            "guidance_scale": 7.5,
            "multi_lingual": "no",
            "panorama": "no",
            "self_attention": "no",
            "upscale": "no",
            "embeddings": "embeddings_model_id",
            "lora": "lora_model_id",
            "webhook": None,
            "track_id": None
        }
        try:
            r = requests.post(uri, headers=headers, data=json.dumps(payload))
            with open("resources/images/img_generated.jpg", "wb") as f:
                f.write(requests.get(r.json()["output"][0]).content)
                print("Image saved to resources/img_generated.jpg")
        except Exception as e:
            print(f"ERROR: Error generating image. {e}")
