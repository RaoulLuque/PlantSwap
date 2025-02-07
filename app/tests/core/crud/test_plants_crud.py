import io
from unittest.mock import patch, PropertyMock

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.crud.plants_crud import create_plant, delete_plant_ad
from app.models import PlantCreate
from app.tests.utils.plants import create_random_plant
from app.tests.utils.users import create_random_user


def test_create_plant_with_image_exception(client: TestClient, db: Session):
    with create_random_user(client, db) as (user, _, _):
        plant_in = PlantCreate(
            name="Test Plant",
            description="This is a test plant",
            tags=["test", "plant"],
        )
        file_content = b"This is a test image file"
        upload_file = UploadFile(
            filename="test_image.png", file=io.BytesIO(file_content)
        )
        with pytest.raises(ValueError) as exception_info:
            create_plant(db, user, plant_in, image=upload_file)
        assert (
            str(exception_info.value)
            == "Failed to upload image: cloud_name is disabled"
        )


def test_delete_plant_ad_with_image_exception(client: TestClient, db: Session):
    with create_random_plant(client, db) as (_, _, _, plant):
        plant.image_url = "https://localhost"
        with patch(
            "app.core.crud.plants_crud.settings.USE_IMAGE_UPLOAD",
            new_callable=PropertyMock,
        ) as a:
            a.return_value = True
            with pytest.raises(ValueError) as exception_info:
                delete_plant_ad(db, plant)
            assert (
                str(exception_info.value)
                == "Failed to delete image: Unknown API key Test"
            )
