from PIL import Image

def apply_weather_effects(img, effect):
    if effect == "fog":
        fog = Image.new("RGBA", img.size, (255, 255, 255, 50))
        img = Image.alpha_composite(img, fog)

    elif effect == "rain":
        # TODO: add rain overlay using OpenCV or custom draw
        pass

    elif effect == "snow":
        # TODO: add snow overlay
        pass

    return img