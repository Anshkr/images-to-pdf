import os
import tempfile

from reportlab.pdfgen import canvas

from utils.constants import *
from utils.template_loader import load_template
from utils.template_engine import TemplateEngine


def generate_pdf(
    images,
    company_name,
    website,
    logo_path,
    template_name,
    images_per_page
):

    # Temporary PDF
    pdf_file = tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False
    )

    pdf_path = pdf_file.name
    pdf_file.close()

    c = canvas.Canvas(
        pdf_path,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT)
    )

    template = load_template(template_name)

    engine = TemplateEngine(
        c,
        template
    )

    total_images = len(images)

    page_number = 1

    for start in range(0, total_images, images_per_page):

        page_images = images[
            start:start + images_per_page
        ]

        # Background
        engine.draw_background(
            PAGE_WIDTH,
            PAGE_HEIGHT
        )

        # Logo
        engine.draw_logo(
            logo_path
        )

        # Company
        engine.draw_company(
            company_name
        )

        # Website
        engine.draw_website(
            website
        )

        # Images
        engine.draw_images(
            page_images,
            images_per_page
        )

        # Page Number
        c.drawRightString(
            PAGE_WIDTH - MARGIN,
            16 * mm,
            f"Page {page_number}"
        )

        c.showPage()

        page_number += 1

    c.save()

    return pdf_path