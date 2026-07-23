from reportlab.lib.utils import ImageReader


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
        page_height
    ):

        self.canvas.drawImage(

            self.template["background"],

            0,

            0,

            width=page_width,

            height=page_height

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


        cfg = self.config.get(
            "logo"
        )


        if not cfg:
            return



        self.canvas.drawImage(

            logo_path,

            cfg["x"],

            cfg["y"],

            width=cfg["width"],

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

        cfg = self.config.get(
            "company_name"
        )


        if not cfg:
            return



        self.canvas.setFont(

            "Helvetica-Bold",

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

        cfg = self.config.get(
            "website"
        )


        if not cfg:
            return



        self.canvas.setFont(

            "Helvetica",

            cfg["font_size"]

        )


        self.canvas.drawString(

            cfg["x"],

            cfg["y"],

            website

        )



    # ----------------------------------------
    # Multiple Images Grid
    # ----------------------------------------

    def draw_images(
        self,
        images,
        images_per_page
    ):


        page_width = self.config["page"]["width"]

        page_height = self.config["page"]["height"]



        margin = self.config["image"]["margin"]



        # Determine Grid

        layouts = {


            1:(1,1),

            2:(2,1),

            3:(3,1),

            4:(2,2),

            6:(3,2),

            9:(3,3)

        }



        cols, rows = layouts[images_per_page]



        cell_width = (

            page_width - (margin*2)

        ) / cols



        cell_height = (

            page_height - (margin*2)

        ) / rows



        for index,image in enumerate(images):


            if index >= images_per_page:

                break



            row = index // cols

            col = index % cols



            x = (

                margin +

                col * cell_width

            )



            y = (

                page_height -

                margin -

                (row+1)*cell_height

            )



            self.draw_single_image(

                image,

                x,

                y,

                cell_width,

                cell_height

            )




    # ----------------------------------------
    # Single Image
    # ----------------------------------------

    def draw_single_image(

        self,

        image,

        x,

        y,

        box_width,

        box_height

    ):


        img_width, img_height = image.size



        ratio = min(

            box_width/img_width,

            box_height/img_height

        )


        new_width = img_width * ratio

        new_height = img_height * ratio



        final_x = (

            x +

            (box_width-new_width)/2

        )


        final_y = (

            y +

            (box_height-new_height)/2

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