import os
import requests
from urllib.request import urlretrieve
from dotenv import load_dotenv
import argparse

load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument('--image-plant', help='Plant name to generate an image for')
opt = parser.parse_args()

def generate_image(name):
    response = requests.post(
        "https://54285744-illusion-diffusion.gateway.alpha.fal.ai/",
        headers={"Authorization": os.getenv("KEY_llusion_diffusio")},
        json={"image_url": "https://storage.googleapis.com/falserverless/illusion-examples/pattern.png",
              "prompt": f"(best quality), (detailed), {name}",
              "negative_prompt": "(lowres, watermark)"}
    )
    return response.json().get("image", {}).get("url")

def identify_plant(image_path):
    with open(image_path, "rb") as img:
        response = requests.post(
            "https://my-api.plantnet.org/v2/identify/all",
            params={"api-key": os.getenv("PLANT_API_KEY")},
            files={"images": img}
        )
    return response.json().get("results", [{}])[4].get("species", {}).get("commonNames", ["Unknown"])[0]

image_url = generate_image(opt.image_plant)
if image_url:
    urlretrieve(image_url, "plant.jpg")
    print("Plant name:", identify_plant("plant.jpg"))
else:
    print("Image generation failed")
