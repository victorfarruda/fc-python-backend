import uuid

import pytest
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateVideoWithoutMedia:
    def test_user_can_create_video_without_media(self) -> None:
        api_client = APIClient()

        list_response = api_client.get("/api/videos/")
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }

        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "Sample Video",
                "description": "A sample video description",
                "launch_year": 2024,
                "opened": False,
                "duration": 120,
                "published": True,
                "rating": "L",
                "categories_id": [],
                "genres_id": [],
                "cast_members_id": [],
            },
            format="json",
        )

        assert HTTP_201_CREATED == create_response.status_code
        created_video_id = create_response.data["id"]

        list_response = api_client.get("/api/videos/")

        assert {
            "data": [
                {
                    "id": created_video_id,
                    "title": "Sample Video",
                    "description": "A sample video description",
                    "launch_year": 2024,
                    "duration": "120.00",
                    "published": True,
                    "rating": "L",
                    "categories_id": [],
                    "genres_id": [],
                    "cast_members_id": [],
                }
            ],
            "meta": {"total": 1, "current_page": 1, "per_page": 2},
        } == list_response.data

        delete_response = api_client.delete(f"/api/videos/{created_video_id}/")
        assert delete_response.status_code == HTTP_204_NO_CONTENT

        list_response = api_client.get("/api/videos/")
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }

    def test_user_can_create_video_without_media_with_categories_genres_and_cast_members(
        self,
    ) -> None:
        api_client = APIClient()

        list_response = api_client.get("/api/videos/")
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }

        create_category_response = api_client.post(
            "/api/categories/",
            data={"name": "Category 1", "description": "Category 1 description"},
            format="json",
        )
        assert create_category_response.status_code == HTTP_201_CREATED
        category_id = create_category_response.data["id"]

        create_genre_response = api_client.post(
            "/api/genres/",
            data={
                "name": "Genre 1",
                "description": "Genre 1 description",
                "categories": [category_id],
            },
            format="json",
        )
        assert create_genre_response.status_code == HTTP_201_CREATED
        genre_id = create_genre_response.data["id"]

        cast_member_id = str(uuid.uuid4())
        create_cast_member_response = api_client.post(
            "/api/cast_members/",
            data={"id": cast_member_id, "name": "Cast Member 1", "type": "ACTOR"},
            format="json",
        )
        assert create_cast_member_response.status_code == HTTP_201_CREATED
        cast_member_id = create_cast_member_response.data["id"]

        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "Sample Video",
                "description": "A sample video description",
                "launch_year": 2024,
                "opened": False,
                "duration": 120,
                "published": True,
                "rating": "L",
                "categories_id": [category_id],
                "genres_id": [genre_id],
                "cast_members_id": [cast_member_id],
            },
            format="json",
        )

        assert HTTP_201_CREATED == create_response.status_code
        created_video_id = create_response.data["id"]
        list_response = api_client.get("/api/videos/")
        assert {
            "data": [
                {
                    "id": created_video_id,
                    "title": "Sample Video",
                    "description": "A sample video description",
                    "launch_year": 2024,
                    "duration": "120.00",
                    "published": True,
                    "rating": "L",
                    "categories_id": [category_id],
                    "genres_id": [genre_id],
                    "cast_members_id": [cast_member_id],
                }
            ],
            "meta": {"total": 1, "current_page": 1, "per_page": 2},
        } == list_response.data

        delete_response = api_client.delete(f"/api/genres/{genre_id}/")
        assert delete_response.status_code == HTTP_204_NO_CONTENT

        list_response = api_client.get("/api/videos/")
        assert {
            "data": [
                {
                    "id": created_video_id,
                    "title": "Sample Video",
                    "description": "A sample video description",
                    "launch_year": 2024,
                    "duration": "120.00",
                    "published": True,
                    "rating": "L",
                    "categories_id": [category_id],
                    "genres_id": [],
                    "cast_members_id": [cast_member_id],
                }
            ],
            "meta": {"total": 1, "current_page": 1, "per_page": 2},
        } == list_response.data

    def test_user_cannot_create_video_without_rating(self) -> None:
        api_client = APIClient()

        list_response = api_client.get("/api/videos/")
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }

        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "Sample Video",
                "description": "A sample video description",
                "launch_year": 2024,
                "opened": False,
                "duration": 120,
                "published": True,
                "categories_id": [],
                "genres_id": [],
                "cast_members_id": [],
            },
            format="json",
        )

        assert HTTP_400_BAD_REQUEST == create_response.status_code
        assert create_response.data == {
            "rating": ["This field is required."],
        }

        list_response = api_client.get("/api/videos/")
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }
