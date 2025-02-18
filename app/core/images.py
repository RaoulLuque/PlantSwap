import cloudinary  # type: ignore
from cloudinary.uploader import upload, destroy  # type: ignore
from cloudinary.exceptions import Error as CloudinaryError  # type: ignore
from fastapi import UploadFile

from app.core.config import settings


def set_cloudinary_config() -> None:
    """
    Set the Cloudinary configuration.
    """
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


def upload_image_to_cloudinary(image: UploadFile, plant_uuid: str) -> str:
    """
    Upload an image to Cloudinary and return the URL. The image has the uuid of the plant as the public_id.
    :param image: The image file to upload
    :param plant_uuid: UUID of the plant to which the image belongs
    :return: URL of the uploaded image
    """
    try:
        result = upload(
            file=image.file,
            resource_type="image",
            folder=f"{settings.CLOUDINARY_FOLDER}",
            public_id=f"{plant_uuid}",
        )
        return result["secure_url"]
    except CloudinaryError as e:
        raise ValueError(f"Failed to upload image: {e}")


def delete_image_from_cloudinary(public_id: str) -> None:
    """
    Delete an image from Cloudinary.
    :param public_id: Public id of the image to delete. It is the uuid of the plant.
    """
    try:
        cloudinary_public_id = f"{settings.CLOUDINARY_FOLDER}/{public_id}"
        destroy(cloudinary_public_id)
    except CloudinaryError as e:
        raise ValueError(f"Failed to delete image: {e}")
