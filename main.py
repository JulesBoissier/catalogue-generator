import os
import base64
import requests
from dotenv import load_dotenv

from typing import List

load_dotenv()

API_KEY = os.getenv("BRIA_API_KEY")
BRIA_URL = "https://engine.prod.bria-api.com/v1/product/lifestyle_shot_by_text"


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def generate_image(image: str, environment: str, num_results: int, **kwargs):

    payload = {
        "file": image,
        "scene_description": environment,
        "placement_type": "manual_placement",
        "num_results": num_results,
        "optimize_description": True,
        "sync": True,
        "mode": "high_control",
    }

    payload.update(kwargs)

    headers = {
        "Content-Type": "application/json",
        "api_token": API_KEY,
    }

    response = requests.post(BRIA_URL, json=payload, headers=headers)

    return response.json()


def fetch_image(bria_response: dict) -> List[str]:
    
    images = []

    for image in bria_response["result"]:

        image_url = image[0]

        img_response = requests.get(image_url)

        # Fetch the image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            img_base64 = base64.b64encode(img_response.content).decode("utf-8")
            images.append(img_base64)

        return images


def run_generation_pipeline(image_path, environments: List[str], **kwargs):

    results = []
    image_base64 = image_to_base64(image_path)

    for environment in environments:
        generation = generate_image(
            image_base64, environment=environment, num_results=3, **kwargs
        )
        images = fetch_image(bria_response=generation)

        results.append({"Environment": environment, "Images": images})

    return results


if __name__ == "__main__":

    path = os.path.join("data", "soap.png")

    environments = [
        "Placed on a sleek, sunlit modern kitchen counter with marble surfaces and subtle reflections",
        "Set on a rustic wooden patio table surrounded by greenery, warm sunlight, and gentle shadows",
        "A professional studio setup with soft lighting, clean background, and perfect focus for product display"
    ]

    extra_args = {
        # "shot_size": [200, 200],
        "manual_placement_selection": ["upper_left", "center_vertical", "bottom_right"],
    }

    results = run_generation_pipeline(
        image_path=path, environments=environments, **extra_args
    )
    # print(results)
