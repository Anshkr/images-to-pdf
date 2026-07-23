from PIL import Image, ImageOps


def smart_resize(
    image,
    max_width=1800,
    max_height=1800
):
    """
    Resize a Pillow Image while preserving aspect ratio.
    Returns a Pillow Image.
    """

    width, height = image.size

    # Don't enlarge small images
    if width <= max_width and height <= max_height:
        return image

    ratio = min(
        max_width / width,
        max_height / height
    )

    new_width = int(width * ratio)
    new_height = int(height * ratio)

    resized = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    return resized