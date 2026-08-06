from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor


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
        images,
        images_per_page
    ):

        layouts = self.config.get("layouts")

        if not layouts:
            return

        boxes = layouts.get(str(images_per_page))

        if not boxes:
            return

        for item, box in zip(images, boxes):

            self.draw_single_image(

                image=item["image"],
                
                product_name=item["name"],

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

        image,
        
        product_name,

        x,

        y,

        box_width,

        box_height

    ):

        img_width, img_height = image.size

        ratio = min(

            box_width / img_width,

            box_height / img_height

        )

        new_width = img_width * ratio

        new_height = img_height * ratio

        final_x = x + (

            (box_width - new_width) / 2

        )

        final_y = y + (

            (box_height - new_height) / 2

        )

        self.canvas.drawImage(

            ImageReader(image),

            final_x,

            final_y,

            width=new_width,

            height=new_height,

            preserveAspectRatio=True,

            mask="auto"

        )
        
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.setFillColor(HexColor("#000000"))
        
        # Position on the "Product Name ______" line
        text_x = x

        text_y = y + box_height - 12
        self.canvas.drawString(
            text_x,
            text_y,
            product_name
        )
        
        # ----------------------------------------
        # Product Name Placeholder
        # ----------------------------------------
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.setFillColor(HexColor("#000000"))
        

        text_x = x
        text_y = y - 15
        
        self.canvas.drawString(
            text_x,
            text_y,
            product_name
        )
          

        
    # ----------------------------------------
    # Footer
    # ----------------------------------------

    def draw_footer(
        self,
        text
    ):

        cfg = self.config.get("footer")

        if not cfg:
            return

        footer_text = cfg.get("text")

        if footer_text:

            text = footer_text

        self.canvas.setFillColor(

            HexColor(
                cfg.get("color", "#666666")
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

            text

        )

    # ----------------------------------------
    # Page Number
    # ----------------------------------------

    def draw_page_number(
        self,
        page_number
    ):

        cfg = self.config.get("page_number")

        if not cfg:
            return

        self.canvas.setFillColor(

            HexColor(
                cfg.get("color", "#666666")
            )

        )

        self.canvas.setFont(

            cfg.get(
                "font",
                "Helvetica"
            ),

            cfg["font_size"]

        )

        text = f"Page {page_number}"

        page_width = self.config["page"]["width"]

        x = page_width - cfg.get(

            "padding_right",

            40

        )

        y = cfg.get(

            "y",

            20

        )

        if cfg.get("align") == "right":

            self.canvas.drawRightString(

                x,

                y,

                text

            )

        else:

            self.canvas.drawString(

                x,

                y,

                text

            )