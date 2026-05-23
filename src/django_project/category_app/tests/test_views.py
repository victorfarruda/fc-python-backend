import uuid

import pytest
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category


@pytest.fixture
def category_movie() -> Category:
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary() -> Category:
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                },
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": 2,
                "total": 2,
            },
        }

        assert HTTP_200_OK == response.status_code
        assert expected_data == response.data

    def test_list_categories_with_pagination(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/?current_page=1&per_page=1"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": 1,
                "total": 2,
            },
        }

        assert HTTP_200_OK == response.status_code
        assert expected_data == response.data


@pytest.mark.django_db
class TestRetriveAPI:
    def test_when_id_is_invalid_return_400(self) -> None:
        url = "/api/categories/123456789/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f"/api/categories/{category_documentary.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active,
            }
        }

        assert status.HTTP_200_OK == response.status_code
        assert expected_data == response.data

    def test_return_404_when_not_exists(
        self,
    ) -> None:

        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)

        assert status.HTTP_404_NOT_FOUND == response.status_code


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Movie description",
            },
        )

        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_when_payload_is_valid_create_category_and_returns_201(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )

        assert status.HTTP_201_CREATED == response.status_code
        print(response.data)
        created_category_id = uuid.UUID(response.data["id"])
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Movie",
            description="Movie description",
        )


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_returns_400(self) -> None:
        url = "/api/categories/123213213123/"  # UUID invalido
        response = APIClient().put(
            url,
            data={
                "name": "",  # Name não pode ser vazio
                "description": "Movie description",
            },
            format="json",
        )

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        } == response.data

    def test_when_payload_is_valid_then_update_category_and_returns_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )

        assert status.HTTP_204_NO_CONTENT == response.status_code
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == category_movie.id
        assert updated_category.name == "Documentary"
        assert updated_category.description == "Documentary description"
        assert updated_category.is_active is True

    def test_when_category_does_not_exist_then_returns_404(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )
        assert status.HTTP_404_NOT_FOUND == response.status_code


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_payload_is_invalid_then_returns_400(self) -> None:
        url = "/api/categories/123213213123/"  # UUID invalido
        response = APIClient().delete(url)

        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_when_category_does_not_exist_then_returns_404(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert status.HTTP_404_NOT_FOUND == response.status_code

    def test_when_payload_is_valid_then_delete_category_and_returns_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert status.HTTP_204_NO_CONTENT == response.status_code
        assert category_repository.list() == []
        assert category_repository.get_by_id(category_movie.id) is None


@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_payload_is_invalid_then_returns_400(self) -> None:
        url = "/api/categories/123213213123/"  # UUID invalido
        response = APIClient().patch(
            url,
            data={
                "description": "Movie description",
            },
            format="json",
        )

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert {"id": ["Must be a valid UUID."]} == response.data

    def test_when_payload_is_valid_then_update_description_from_category_and_returns_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "description": "New Movie Description",
            },
        )

        assert status.HTTP_204_NO_CONTENT == response.status_code
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == category_movie.id
        assert updated_category.name == category_movie.name
        assert updated_category.description == "New Movie Description"
        assert updated_category.is_active is category_movie.is_active

    def test_when_payload_is_valid_then_update_name_from_category_and_returns_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "name": "New Documentary",
            },
        )

        assert status.HTTP_204_NO_CONTENT == response.status_code
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == category_movie.id
        assert updated_category.name == "New Documentary"
        assert updated_category.description == category_movie.description
        assert updated_category.is_active is category_movie.is_active

    def test_when_payload_is_valid_then_update_is_active_to_false_from_category_and_returns_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "is_active": False,
            },
        )

        assert status.HTTP_204_NO_CONTENT == response.status_code
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == category_movie.id
        assert updated_category.name == category_movie.name
        assert updated_category.description == category_movie.description
        assert updated_category.is_active is False

    def test_when_payload_is_valid_then_update_is_active_to_true_from_category_and_returns_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "is_active": True,
            },
        )

        assert status.HTTP_204_NO_CONTENT == response.status_code
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == category_movie.id
        assert updated_category.name == category_movie.name
        assert updated_category.description == category_movie.description
        assert updated_category.is_active is True

    def test_when_category_does_not_exist_then_returns_404(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().patch(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )
        assert status.HTTP_404_NOT_FOUND == response.status_code
