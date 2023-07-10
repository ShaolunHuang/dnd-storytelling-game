import requests
import json
import os
import time


class ImageGenerator:

    def __init__(self):
        self.api_key = os.getenv("STABLE_DIFFUSION_API_KEY")

    def get_image(self, prompt, counter):
        uri = "https://stablediffusionapi.com/api/v3/dreambooth"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "key": self.api_key,
            "model_id": "anything-v5",
            "prompt": prompt,
            "negative_prompt": "",
            "width": "400",
            "height": "400",
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
        except Exception as e:
            print(f"ERROR: Error generating image. {e}")
            return
        if r.status_code != 200:
            print(f"ERROR: Error generating image. Invalid response code {r.status_code}")
            return
        else:
            if "output" in r.json() and len(r.json()["output"]) > 0:
                with open(f"resources/images/img_generated_{counter}.png", "wb") as f:
                        f.write(requests.get(r.json()["output"][0]).content)
                        print("Image saved to resources/img_generated.png")
            else:
                if "id" not in r.json():
                    print("ERROR: Error generating image. No ID in response.")
                    return
                id = r.json()["id"]
                count = 0
                while "status" in r.json() and r.json()["status"] == "processing" and count < 20:
                    uri = "https://stablediffusionapi.com/api/v4/dreambooth/fetch"
                    payload = {
                        "key": self.api_key,
                        "request_id": id
                    }
                    try:
                        r = requests.post(uri, headers=headers, data=json.dumps(payload))
                    except Exception as e:
                        print(f"ERROR: Error generating image. {e}")
                        return
                    if "output" in r.json() and len(r.json()["output"]) > 0:
                        with open(f"resources/images/img_generated_{counter}.png", "wb") as f:
                                f.write(requests.get(r.json()["output"][0]).content)
                                print("Image saved to resources/img_generated.png")
                        break
                    time.sleep(1)
                    count += 1
                print("ERROR: Wait time too long.")
