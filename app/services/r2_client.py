from botocore.exceptions import ClientError
from fastapi import UploadFile
from app.core.r2_client import r2_client, R2_BUCKET_NAME, R2_PUBLIC_URL, R2_IMAGE_BUCKET_NAME
import uuid
from io import BytesIO


async def upload_image_to_r2(upload_file: UploadFile) -> str:
    """
    Uploads an image file to R2 and returns the public URL (non-expiring).
    Reads file bytes async and resets file pointer for other services.
    """
    try:
        # Read file bytes correctly (async)
        file_bytes = await upload_file.read()

        # Get file extension and generate unique name
        ext = upload_file.filename.split(".")[-1] if upload_file.filename else "bin"
        unique_name = f"{uuid.uuid4()}.{ext}"

        # Upload to R2 using BytesIO
        r2_client.upload_fileobj(
            BytesIO(file_bytes),
            R2_IMAGE_BUCKET_NAME,
            unique_name
        )

        # Reset file pointer so other services can read it again
        upload_file.file.seek(0)

        # Generate public URL (non-expiring)
        url = f"{R2_PUBLIC_URL}/{unique_name}"

        print(f"R2 upload successful: {unique_name}")
        return url

    except ClientError as e:
        print("R2 upload failed:", e)
        raise Exception(f"R2 Upload failed: {e.response['Error']['Message']}")
    except Exception as e:
        print("R2 upload failed:", e)
        raise Exception(f"R2 Upload failed: {str(e)}")


async def upload_to_r2(file: UploadFile) -> str:
    """
    Uploads a file object to R2 and returns the filename.
    """

    # Only check filename, NOT instanceof
    if not hasattr(file, "filename") or not file.filename:
        raise ValueError("upload_to_r2 received invalid file object (missing filename)")

    try:
        ext = file.filename.split(".")[-1]
        unique_name = f"{uuid.uuid4()}.{ext}"

        r2_client.upload_fileobj(
            file.file,
            R2_BUCKET_NAME,
            unique_name
        )
        print(f"R2 upload successful: {unique_name}")
        return unique_name

    except ClientError as e:
        print("R2 upload failed:", e)
        raise Exception(f"R2 Upload failed: {e.response['Error']['Message']}")


async def generate_r2_download_url(filename: str, expiry: int = 3600) -> str:
    """
    Generates a presigned download URL valid for `expiry` seconds.
    """
    try:
        url = r2_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": R2_BUCKET_NAME, "Key": filename},
            ExpiresIn=expiry,
        )
        return url
    except ClientError as e:
        raise Exception(f"R2 URL generation failed: {e.response['Error']['Message']}")


async def delete_from_r2(filename: str) -> None:
    """
    Deletes a file from the R2 bucket.
    """
    try:
        r2_client.delete_object(Bucket=R2_BUCKET_NAME, Key=filename)
    except ClientError as e:
        raise Exception(f"R2 deletion failed: {e.response['Error']['Message']}")



