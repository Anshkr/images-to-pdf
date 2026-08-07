import os
from collections import Counter
from utils.models import Product


def analyze(image, filename, details=None):
    width, height = image.size

    aspect_ratio = width / height if height else 1.0

    orientation = (
        "landscape"
        if width >= height
        else "portrait"
    )

    small = image.resize((50, 50))
    pixels = list(small.getdata())
    dominant = Counter(pixels).most_common(1)[0][0]

    base_name = os.path.splitext(filename)[0]

    default_product_name = (
        base_name.replace("_", " ")
        .replace("-", " ")
        .title()
    )

    default_description = (
        f"Premium quality {default_product_name.lower()}."
    )

    if details:
        product_name = details.get("product_name", default_product_name)
        description = details.get("description", default_description)
        category = details.get("category", "General")
        material = details.get("material", "Unknown")
        color = details.get("color", "Unknown")
    else:
        product_name = default_product_name
        description = default_description
        category = "General"
        material = "Unknown"
        color = "Unknown"

    sku = base_name.upper().replace("-", "_").replace(" ", "_")

    # Use fallback if Gemini returns empty strings
    if details:
        product_name = details.get("product_name") or default_product_name
        description = details.get("description") or default_description
        category = details.get("category") or "General"
        material = details.get("material") or "Unknown"
        color = details.get("color") or "Unknown"
    else:
        product_name = default_product_name
        description = default_description
        category = "General"
        material = "Unknown"
        color = "Unknown"

    return Product(
        image=image,
        filename=filename,
        product_name=product_name,
        category=category,
        material=material,
        color=color,
        description=description,
        sku=sku,

        width=width,
        height=height,
        aspect_ratio=aspect_ratio,
        orientation=orientation,

        visual_weight=1.0,
        dominant_color=dominant
    )