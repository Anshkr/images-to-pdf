from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from utils.layout_engine import LayoutEngine
from textwrap import wrap
import os

class TemplateEngine:

    def __init__(self, canvas, template):

        self.canvas = canvas
        self.template = template
        self.config = template["config"]

    # ----------------------------------------
    # Background
    # ----------------------------------------

    def draw_background(
        self,
        page_width,
        page_height,
        custom_background=None
    ):

        # If user uploaded Canva template use it
        if custom_background:

            bg = custom_background

        else:

            bg = self.template["background"]

        self.canvas.drawImage(

            bg,

            0,

            0,

            width=page_width,

            height=page_height,

            preserveAspectRatio=False,

            mask="auto"

        )

    # ----------------------------------------
    # Logo
    # ----------------------------------------

    def draw_logo(
        self,
        logo_path
    ):

        if not logo_path:
            return

        cfg = self.config.get("logo")

        if not cfg:
            return

        self.canvas.drawImage(

            logo_path,

            cfg["x"],

            cfg["y"],

            width=cfg["width"],

            height=cfg.get("height"),

            preserveAspectRatio=True,

            mask="auto"

        )

    # ----------------------------------------
    # Company Name
    # ----------------------------------------

    def draw_company(
        self,
        company
    ):

        cfg = self.config.get("company_name")

        if not cfg:
            return

        self.canvas.setFillColor(

            HexColor(
                cfg.get("color", "#000000")
            )

        )

        self.canvas.setFont(

            cfg.get(
                "font",
                "Helvetica-Bold"
            ),

            cfg["font_size"]

        )

        self.canvas.drawString(

            cfg["x"],

            cfg["y"],

            company

        )

    # ----------------------------------------
    # Website
    # ----------------------------------------

    def draw_website(
        self,
        website
    ):

        cfg = self.config.get("website")

        if not cfg:
            return

        self.canvas.setFillColor(

            HexColor(
                cfg.get("color", "#555555")
            )

        )

        self.canvas.setFont(

            cfg.get(
                "font",
                "Helvetica"
            ),

            cfg["font_size"]

        )

        self.canvas.drawString(

            cfg["x"],

            cfg["y"],

            website

        )

    # ----------------------------------------
    # Images
    # ----------------------------------------

    def draw_images(
        self,
        products,
        images_per_page
    ):

        layout_engine = LayoutEngine()

        layout = layout_engine.generate_layout(products)

        for product, box in zip(products, layout):

            self.draw_single_image(

                product=product,

                x=box["x"],

                y=box["y"],

                box_width=box["width"],

                box_height=box["height"]

            )

    # ----------------------------------------
    # Single Image
    # ----------------------------------------

    def draw_single_image(
        self,
        product,
        x,
        y,
        box_width,
        box_height
    ):

        image = product.image
        product_name = (
            product.product_name.strip()
            if product.product_name
            else os.path.splitext(product.filename)[0].replace("_", " ").title()
        )
        description = (
            product.description.strip()
            if product.description
            else "No AI description available"
        )

        # ----------------------------------------
        # Shadow
        # ----------------------------------------

        self.canvas.setFillColor(HexColor("#EAEAEA"))

        self.canvas.roundRect(
            x + 3,
            y - 3,
            box_width,
            box_height,
            10,
            fill=1,
            stroke=0
        )

        # ----------------------------------------
        # Card
        # ----------------------------------------

        self.canvas.setFillColor(HexColor("#FFFFFF"))
        self.canvas.setStrokeColor(HexColor("#DDDDDD"))

        self.canvas.roundRect(
            x,
            y,
            box_width,
            box_height,
            10,
            fill=1,
            stroke=1
        )

        # ----------------------------------------
        # Image Area
        # ----------------------------------------

        CARD_PADDING = 15
        TOP_TEXT = 45
        BOTTOM_TEXT = 95

        image_x = x + CARD_PADDING
        image_y = y + BOTTOM_TEXT

        image_width = box_width - (CARD_PADDING * 2)
        image_height = box_height - TOP_TEXT - BOTTOM_TEXT

        img_width, img_height = image.size

        ratio = min(
            image_width / img_width,
            image_height / img_height
        )

        new_width = img_width * ratio
        new_height = img_height * ratio

        final_x = image_x + (image_width - new_width) / 2
        final_y = image_y + (image_height - new_height) / 2

        # ----------------------------------------
        # Draw Image
        # ----------------------------------------

        self.canvas.drawImage(
            ImageReader(image),
            final_x,
            final_y,
            width=new_width,
            height=new_height,
            preserveAspectRatio=True,
            mask="auto"
        )

        # ----------------------------------------
        # Divider
        # ----------------------------------------

        divider_y = y + 38

        self.canvas.setStrokeColor(HexColor("#EEEEEE"))

        self.canvas.line(
            x + 12,
            divider_y,
            x + box_width - 12,
            divider_y
        )

        # ----------------------------------------
        # Product Name
        # ----------------------------------------

        self.canvas.setFillColor(HexColor("#222222"))
        self.canvas.setFont("Helvetica-Bold", 11)

        name_lines = wrap(product_name, width=22)

        text_y = y + 22

        for line in reversed(name_lines[:2]):
            self.canvas.drawCentredString(
                x + box_width / 2,
                text_y,
                line
            )
            text_y += 12

        # ----------------------------------------
        # Description
        # ----------------------------------------

        self.canvas.setFillColor(HexColor("#666666"))
        self.canvas.setFont("Helvetica", 8)

        desc_lines = wrap(description, width=34)

        desc_y = y + 8

        for line in reversed(desc_lines[:2]):
            self.canvas.drawCentredString(
                x + box_width / 2,
                desc_y,
                line
            )
            desc_y += 10
    
    def draw_page_number(self, page_number):
    
        cfg = self.config.get("page_number")

        if not cfg:
            return

        self.canvas.setFillColor(
            HexColor(cfg.get("color", "#666666"))
        )

        self.canvas.setFont(
            cfg.get("font", "Helvetica"),
            cfg.get("font_size", 10)
        )

        text = f"Page {page_number}"

        page_width = self.config["page"]["width"]

        x = page_width - cfg.get("padding_right", 40)
        y = cfg.get("y", 20)

        if cfg.get("align") == "right":
            self.canvas.drawRightString(x, y, text)
        else:
            self.canvas.drawString(x, y, text)