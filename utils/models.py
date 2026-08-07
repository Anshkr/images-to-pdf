from dataclasses import dataclass
from PIL import Image


@dataclass
class Product:
    # Image
    image: Image.Image
    filename: str

    # Basic Info
    product_name: str
    description: str = ""

    # AI Metadata
    category: str = ""
    material: str = ""
    color: str = ""
    sku: str = ""

    # Image Metadata
    width: int = 0
    height: int = 0
    aspect_ratio: float = 1.0
    orientation: str = "portrait"

    visual_weight: float = 1.0
    dominant_color: tuple = (255, 255, 255)