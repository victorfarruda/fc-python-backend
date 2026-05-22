import uuid

import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCastMember:
    def test_user_can_create_and_edit_cast_member(self) -> None:
        api_client = APIClient()

        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {"data": []}

        create_response = api_client.post(
            "/api/cast_members/",
            data={
                "id": str(uuid.uuid4()),
                "name": "Victor",
                "type": "DIRECTOR",
            },
        )

        assert HTTP_201_CREATED == create_response.status_code
        created_cast_member_id = create_response.data["id"]

        list_response = api_client.get("/api/cast_members/")
        assert {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "Victor",
                    "type": "DIRECTOR",
                }
            ]
        } == list_response.data

        update_request = api_client.put(
            f"/api/cast_members/{created_cast_member_id}/",
            data={
                "name": "Other name",
                "type": "ACTOR",
            },
        )

        assert HTTP_204_NO_CONTENT == update_request.status_code

        list_response = api_client.get("/api/cast_members/")
        assert {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "Other name",
                    "type": "ACTOR",
                }
            ]
        } == list_response.data
