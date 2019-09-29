from PIL import Image
import requests
from io import BytesIO


def load_image(type, path):
    if type == 'local':
        return load_local(path)
    else:
        return load_remote(path)


def load_remote(path):
    response = requests.get(path)
    img = Image.open(BytesIO(response.content))
    return img


def load_local(path):
    img = Image.open(path)
    return img
