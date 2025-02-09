import io
import uuid
from unittest.mock import patch

import cloudinary
import pytest
from fastapi import UploadFile

from app.core.config import settings
from app.core.images import (
    set_cloudinary_config,
    upload_image_to_cloudinary,
    delete_image_from_cloudinary,
)


def test_set_cloudinary_config():
    set_cloudinary_config()
    assert settings.CLOUDINARY_CLOUD_NAME == cloudinary.config().cloud_name
    assert settings.CLOUDINARY_API_KEY == cloudinary.config().api_key
    assert settings.CLOUDINARY_API_SECRET == cloudinary.config().api_secret
    assert cloudinary.config().secure is True


def test_upload_image_to_cloudinary():
    file_content = b"This is a test image file"
    upload_file = UploadFile(filename="test_image.png", file=io.BytesIO(file_content))
    plant_uuid = str(uuid.UUID)

    mocked_upload_response = {"secure_url": "https://localhost"}
    with patch("app.core.images.upload", return_value=mocked_upload_response):
        upload_image_to_cloudinary(upload_file, plant_uuid)


def test_upload_image_to_cloudinary_invalid_image_file_exception():
    file_content = b"This is a test image file"
    upload_file = UploadFile(filename="test_image.png", file=io.BytesIO(file_content))
    plant_uuid = ""

    with pytest.raises(ValueError) as exception_info:
        upload_image_to_cloudinary(upload_file, plant_uuid)

    assert (str(exception_info.value)).startswith("Failed to upload image:")


def test_delete_image_from_cloudinary():
    public_id = str(uuid.UUID)

    with patch("app.core.images.destroy") as mocked_destroy:
        delete_image_from_cloudinary(public_id)

    mocked_destroy.assert_called_once_with(public_id)


def test_delete_image_from_cloudinary_exception():
    public_id = str(uuid.UUID)

    with patch("app.core.images.destroy", side_effect=cloudinary.exceptions.Error):
        with pytest.raises(ValueError) as exception_info:
            delete_image_from_cloudinary(public_id)

    assert (str(exception_info.value)).startswith("Failed to delete image:")
