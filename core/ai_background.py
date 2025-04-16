import openai, os, uuid, requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_background(prompt="realistic forest", size="512x512", save_dir="backgrounds"):
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY is missing or empty")

    response = openai.images.generate(model="dall-e-3", prompt=prompt, n=1, size=size)
    url = response.data[0].url
    img = Image.open(BytesIO(requests.get(url).content))

    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"bg_{uuid.uuid4().hex[:6]}.png")
    img.save(path)
    return path