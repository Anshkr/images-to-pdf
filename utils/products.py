from dataclasses import dataclass
from PIL import Image


@dataclass
class Product:
    image: Image.Image
    filename: str
    product_name: str

    width: int
    height: int
    aspect_ratio: float
    orientation: str

    visual_weight: float
    dominant_color: tuple

    category: str = ""
    material: str = ""
    color: str = ""
    description: str = ""
    sku: str = ""