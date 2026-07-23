from fastapi import UploadFile

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def validate_image(file: UploadFile):

    filename = file.filename.lower()

    for ext in ALLOWED_EXTENSIONS:

        if filename.endswith(ext):
            return True

    return False