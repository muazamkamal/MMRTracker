# Name: Muazam Kamal
# File: imageProcess.py
# Purpose: Loading and tweaking the image for a better OCR performance.

from PIL import Image
from PIL import ImageOps

def loadImage(file):
    try:
        # Conversion to remove alpha channel, because invert does not work on alpha channel.
        image = Image.open(file).convert("RGB")

        width, height = image.size

        ratio = round(width/height, 2)

        if ratio < 1.78 or ratio > 1.78:
            print("fatal: Screenshot aspect ratio did not match.")

            image = None
        else:
            topX = 0.73 * width
            topY = 0.17 * height

            bottomX = 0.86 * width
            bottomY = 0.25 * height

            image = image.crop((topX, topY, bottomX, bottomY))
            image = ImageOps.invert(image)

            newSize = tuple(2*x for x in image.size)

            image = image.resize(newSize, Image.ANTIALIAS)

        return image
    except (FileNotFoundError, PermissionError) as ex:
        print("fatal: " + ex.strerror)