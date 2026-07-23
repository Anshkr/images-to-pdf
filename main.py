import os
import traceback
import tempfile
from typing import List

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    BackgroundTasks
)
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.validator import validate_image
from utils.image_processor import process_image
from utils.pdf_generator import generate_pdf
from utils.template_loader import load_template

app = FastAPI(
    title="Dynamic Catalogue Generator API",
    version="2.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "project": "Dynamic Catalogue Generator",
        "version": "2.2.0"
    }


# --------------------------------------------------
# Generate Catalogue PDF
# --------------------------------------------------

@app.post("/api/generate-pdf")
async def generate_pdf_api(

    background_tasks: BackgroundTasks,

    company_name: str = Form(...),

    website: str = Form(...),

    template_name: str = Form(...),

    images_per_page: int = Form(...),

    logo: UploadFile | None = File(None),

    images: List[UploadFile] = File(...)

):

    # --------------------------------------------------
    # Validate Images Per Page
    # --------------------------------------------------

    if images_per_page not in [1, 2, 3, 4, 6, 9]:

        return JSONResponse(

            status_code=400,

            content={

                "error": "images_per_page must be one of: 1,2,3,4,6,9"

            }

        )

    # --------------------------------------------------
    # Validate Template
    # --------------------------------------------------

    template = load_template(template_name)

    if template is None:

        return JSONResponse(

            status_code=400,

            content={

                "error": f"Template '{template_name}' not found."

            }

        )

    logo_path = None

    try:

        # --------------------------------------------------
        # Save Logo Temporarily
        # --------------------------------------------------

        if logo and logo.filename:

            suffix = os.path.splitext(logo.filename)[1]

            temp_logo = tempfile.NamedTemporaryFile(

                suffix=suffix,

                delete=False

            )

            temp_logo.write(await logo.read())

            temp_logo.close()

            logo_path = temp_logo.name

        # --------------------------------------------------
        # Process Images (Memory Only)
        # --------------------------------------------------

        processed_images = []

        for image in images:

            if not validate_image(image):

                continue

            processed = process_image(image)

            processed_images.append(processed)

        # --------------------------------------------------
        # No Images
        # --------------------------------------------------

        if len(processed_images) == 0:

            return JSONResponse(

                status_code=400,

                content={

                    "error": "No valid images uploaded."

                }

            )

        # --------------------------------------------------
        # Generate PDF
        # --------------------------------------------------

        pdf_path = generate_pdf(

            images=processed_images,

            company_name=company_name,

            website=website,

            logo_path=logo_path,

            template_name=template_name,

            images_per_page=images_per_page

        )

        # --------------------------------------------------
        # Verify PDF
        # --------------------------------------------------

        if not os.path.exists(pdf_path):

            return JSONResponse(

                status_code=500,

                content={

                    "error": "PDF generation failed."

                }

            )

        # --------------------------------------------------
        # Cleanup After Response
        # --------------------------------------------------

        if logo_path:

            background_tasks.add_task(

                os.remove,

                logo_path

            )

        background_tasks.add_task(

            os.remove,

            pdf_path

        )

        # --------------------------------------------------
        # Return PDF
        # --------------------------------------------------

        return FileResponse(

            path=pdf_path,

            media_type="application/pdf",

            filename="catalogue.pdf",

            background=background_tasks

        )

    except Exception as e:

        traceback.print_exc()

        if logo_path and os.path.exists(logo_path):
            os.remove(logo_path)

        return JSONResponse(

            status_code=500,

            content={

                "error": str(e),

                "trace": traceback.format_exc()

            }

        )