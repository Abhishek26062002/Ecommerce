import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os
from fastapi import FastAPI, File, UploadFile
import tempfile

load_dotenv()

CLOUDINARY_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

cloudinary.config( 
    cloud_name = CLOUDINARY_NAME, 
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET, 
    secure=True
)

async def upload_file_to_cloudinary(upload_file: UploadFile):
    try:
        # Read file bytes correctly (async)
        file_bytes = await upload_file.read()

        # Write into temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        # Upload to Cloudinary
        response = cloudinary.uploader.upload(tmp_path)

        # Remove temp file
        os.remove(tmp_path)

        # Reset file pointer so R2 can read it again
        upload_file.file.seek(0)

        return response

    except Exception as e:
        print("Cloudinary upload failed:", e)
        return None
