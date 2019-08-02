# Name: Muazam Kamal
# File: imageProcess.py
# Purpose: Loading and tweaking the image for a better OCR performance.

from PIL import Image
from PIL import ImageOps
import os

def file_date(file):
    return os.path.getmtime(file)

def load_image(file):
    try:
        # Conversion to remove alpha channel, because invert does not work on alpha channel.
        image = Image.open(file).convert("RGB")

        width, height = image.size

        ratio = round(width/height, 2)

        if ratio < 1.78 or ratio > 1.78:
            print("fatal: Screenshot aspect ratio did not match.")

            image = None
        else:
            top_X = 0.73 * width
            top_Y = 0.17 * height

            bottom_X = 0.86 * width
            bottom_Y = 0.25 * height

            image = image.crop((top_X, top_Y, bottom_X, bottom_Y))
            image = ImageOps.invert(image)

            new_size = tuple(2*x for x in image.size)

            image = image.resize(new_size, Image.ANTIALIAS)

        return image
    except (FileNotFoundError, PermissionError) as e:
        print("fatal: " + e.strerror)