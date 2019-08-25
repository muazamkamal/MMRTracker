# Name: Muazam Kamal
# File: imageProcess.py
# Purpose: Loading and tweaking the image for a better OCR performance.

from PIL import Image
from PIL import ImageOps
import os
import platform

def file_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

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
            top_X = 0.71 * width
            top_Y = 0.17 * height

            bottom_X = 0.86 * width
            bottom_Y = 0.24 * height

            image = image.crop((top_X, top_Y, bottom_X, bottom_Y))
            image = ImageOps.invert(image)

            new_size = tuple(2*x for x in image.size)

            image = image.resize(new_size, Image.ANTIALIAS)

        return image
    except (FileNotFoundError, PermissionError) as e:
        print("fatal: " + e.strerror)