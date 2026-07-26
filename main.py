import os
import logging
import uuid
import time
import threading
import traceback
import tempfile
from typing import List

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.validator import validate_image
from utils.image_processor import process_image
from utils.pdf_generator import generate_pdf
from utils.template_loader import load_template
from dotenv import load_dotenv
load_dotenv()

origins = os.getenv(
    "ALLOWED_ORIGINS",
    "https://pdfplus.in,https://www.pdfplus.in"
).split(",")

app = FastAPI(
    title="Dynamic Catalogue Generator API",
    version="3.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("generated", exist_ok=True)


# --------------------------------------------------
# Auto Delete PDF after 10 minutes
# --------------------------------------------------

def delete_pdf(path):

    DELETE_TIME = int(os.getenv("PDF_DELETE_TIME", "600"))

    time.sleep(DELETE_TIME)

    if os.path.exists(path):

        os.remove(path)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {

        "status": "running",

        "project": "Dynamic Catalogue Generator",

        "version": os.getenv("APP_VERSION", "3.1.0")

    }


# --------------------------------------------------
# Generate PDF
# --------------------------------------------------

@app.post("/api/generate-pdf")
async def generate_pdf_api(

    company_name: str = Form(...),

    website: str = Form(...),

    template_name: str = Form(...),

    images_per_page: int = Form(...),

    logo: UploadFile | None = File(None),

    template_file: UploadFile | None = File(None),

    images: List[UploadFile] = File(...)

):

    if images_per_page not in [1,2,3,4,6,9]:

        return JSONResponse(

            status_code=400,

            content={

                "error":"images_per_page must be one of: 1,2,3,4,6,9"

            }

        )

    if template_name != "custom":
    
        template = load_template(template_name)

        if template is None:

            return JSONResponse(

                status_code=400,

                content={

                    "error": f"Template '{template_name}' not found."

                }

            )
    if template_name == "custom":
    
        if not template_file or not template_file.filename:

            return JSONResponse(

                status_code=400,

                content={

                    "error": "Please upload a custom template image."

                }

            )

    logo_path = None

    custom_background = None

    try:

        # ------------------------------------------
        # Save Logo
        # ------------------------------------------

        if logo and logo.filename:

            suffix = os.path.splitext(logo.filename)[1]

            temp_logo = tempfile.NamedTemporaryFile(

                suffix=suffix,

                delete=False

            )

            temp_logo.write(await logo.read())

            temp_logo.close()

            logo_path = temp_logo.name


        # ------------------------------------------
        # Save Uploaded Canva Template
        # ------------------------------------------

        if (
            template_name == "custom"
            and template_file
            and template_file.filename
        ):

            suffix = os.path.splitext(template_file.filename)[1]

            temp_template = tempfile.NamedTemporaryFile(
                suffix=suffix,
                delete=False
            )

            temp_template.write(await template_file.read())
            temp_template.close()

            custom_background = temp_template.name


        # ------------------------------------------
        # Process Images
        # ------------------------------------------

        processed_images = []

        for image in images:

            if not validate_image(image):

                continue

            processed_images.append(

                process_image(image)

            )

        if len(processed_images) == 0:

            return JSONResponse(

                status_code=400,

                content={

                    "error":"No valid images uploaded."

                }

            )
        # ------------------------------------------
        # Generate PDF
        # ------------------------------------------

        job_id = str(uuid.uuid4())

        pdf_path = os.path.join(

            "generated",

            f"{job_id}.pdf"

        )
        print("Received template_name:", template_name)

        generate_pdf(

            images=processed_images,

            company_name=company_name,

            website=website,

            logo_path=logo_path,

            template_name=template_name,

            custom_background=custom_background,

            images_per_page=images_per_page,

            output_path=pdf_path

        )

        if not os.path.exists(pdf_path):

            return JSONResponse(

                status_code=500,

                content={

                    "error":"PDF generation failed."

                }

            )

        # ------------------------------------------
        # Auto Delete after 10 minutes
        # ------------------------------------------

        threading.Thread(

            target=delete_pdf,

            args=(pdf_path,),

            daemon=True

        ).start()

        # ------------------------------------------
        # Cleanup Temporary Files
        # ------------------------------------------

        if logo_path and os.path.exists(logo_path):

            os.remove(logo_path)

        if custom_background and os.path.exists(custom_background):
    
            os.remove(custom_background)

        # ------------------------------------------
        # Return Preview & Download URLs
        # ------------------------------------------

        return {

            "success": True,

            "job_id": job_id,

            "preview_url": f"/api/preview/{job_id}",

            "download_url": f"/api/download/{job_id}"

        }

    except Exception as e:

        logging.error(traceback.format_exc())

        if logo_path and os.path.exists(logo_path):

            os.remove(logo_path)

        if custom_background and os.path.exists(custom_background):

            os.remove(custom_background)

        return JSONResponse(

            status_code=500,

            content={

                "error": str(e),

                "trace": traceback.format_exc()

            }

        )
        # --------------------------------------------------
# Preview PDF
# --------------------------------------------------

@app.get("/api/preview/{job_id}")
def preview_pdf(job_id: str):

    pdf_path = os.path.join(

        "generated",

        f"{job_id}.pdf"

    )

    if not os.path.exists(pdf_path):

        return JSONResponse(

            status_code=404,

            content={

                "error":"PDF not found."

            }

        )

    return FileResponse(

        path=pdf_path,

        media_type="application/pdf"

    )


# --------------------------------------------------
# Download PDF
# --------------------------------------------------

@app.get("/api/download/{job_id}")
def download_pdf(job_id: str):

    pdf_path = os.path.join(

        "generated",

        f"{job_id}.pdf"

    )

    if not os.path.exists(pdf_path):

        return JSONResponse(

            status_code=404,

            content={

                "error":"PDF not found."

            }

        )

    return FileResponse(

        path=pdf_path,

        media_type="application/pdf",

        filename="catalogue.pdf"

    )