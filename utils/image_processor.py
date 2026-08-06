import os
from PIL import Image, ImageOps
from io import BytesIO

from utils.image_optimizer import smart_resize


def process_image(upload_file):
    """
    Convert UploadFile directly into an optimized Pillow Image.
    """

    image = Image.open(upload_file.file)

    image = ImageOps.exif_transpose(image)

    image = image.convert("RGB")

    image = smart_resize(image)

    return {
        "image": image,
        "name": os.path.splitext(upload_file.filename)[0]
    }