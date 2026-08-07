import os
from collections import Counter

from utils.models import Product


def analyze(image, filename, details=None):
    """
    Analyze processed image and create a Product object.
    Uses AI details when available, otherwise falls back
    to filename-derived information.
    """

    width, height = image.size

    aspect_ratio = width / height if height else 1.0

    orientation = (
        "landscape"
        if width >= height
        else "portrait"
    )

    # ----------------------------------------
    # Dominant Color
    # ----------------------------------------

    small = image.resize((50, 50))
    pixels = list(small.getdata())
    dominant = Counter(pixels).most_common(1)[0][0]

    # ----------------------------------------
    # Default values
    # ----------------------------------------

    base_name = os.path.splitext(filename)[0]

    default_product_name = (
        base_name.replace("_", " ")
        .replace("-", " ")
        .title()
    )

    default_description = (
        f"Premium quality {default_product_name.lower()}."
    )

    default_category = "General"

    default_material = "Unknown"

    default_color = "Unknown"

    sku = (
        base_name.upper()
        .replace(" ", "_")
        .replace("-", "_")
    )

    # ----------------------------------------
    # AI values (if available)
    # ----------------------------------------

    if details:
        product_name = details.get(
            "product_name",
            default_product_name
        )

        description = details.get(
            "description",
            default_description
        )

        category = details.get(
            "category",
            default_category
        )

        material = details.get(
            "material",
            default_material
        )

        color = details.get(
            "color",
            default_color
        )

    else:
        product_name = default_product_name
        description = default_description
        category = default_category
        material = default_material
        color = default_color

    # ----------------------------------------
    # Create Product
    # ----------------------------------------

    return Product(
        image=image,
        filename=filename,

        product_name=product_name,
        description=description,
        category=category,
        material=material,
        color=color,
        sku=sku,

        width=width,
        height=height,
        aspect_ratio=aspect_ratio,
        orientation=orientation,

        visual_weight=1.0,
        dominant_color=dominant
    )