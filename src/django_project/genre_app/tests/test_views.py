from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category
from src.django_project.genre_app.repository import DjangoORMGenreRepository


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


@pytest.fixture
def genre_romance(category_documentary, category_movie) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_documentary.id, category_movie.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(name="Drama", is_active=True, categories=set())


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
        self,
        genre_romance: Genre,
        genre_drama: Genre,
        genre_repository: DjangoORMGenreRepository,
        category_repository: DjangoORMCategoryRepository,
        category_documentary: Category,
        category_movie: Category,
    ):
        category_repository.save(category_documentary)
        category_repository.save(category_movie)
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        url = "/api/genres/"

        response = APIClient().get(url)

        expected_response = {
            "data": [
                {
                    "id": str(genre_romance.id),
                    "name": "Romance",
                    "is_active": True,
                    "categories": [
                        str(category_documentary.id),
                        str(category_movie.id),
                    ],
                },
                {
                    "id": str(genre_drama.id),
                    "name": "Drama",
                    "is_active": True,
                    "categories": [],
                },
            ]
        }
        assert response.status_code == HTTP_200_OK
        assert expected_response == response.data


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_associated_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/genres/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [str(category_movie.id), str(category_documentary.id)],
        }

        response = APIClient().post(url, data=data, format="json")

        assert response.status_code == HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["name"] == "Drama"
        assert response.data["is_active"] is True
        assert set(response.data["categories"]) == {
            str(category_movie.id),
            str(category_documentary.id),
        }

        created_genre_id = response.data["id"]
        saved_genre = genre_repository.get_by_id(created_genre_id)
        assert saved_genre is not None
        assert saved_genre.name == "Drama"
        assert saved_genre.is_active is True
        assert set(saved_genre.categories) == {
            category_movie.id,
            category_documentary.id,
        }


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories_id": [category_documentary.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories_id": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories_id": [uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories_id": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_genre_does_not_exist_then_return_404(self):
        url = "/api/genres/00000000-0000-0000-0000-000000000000/"

        response = APIClient().delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND

    def test_when_pk_is_invlid_then_return_400(self):
        url = "/api/genres/invalid-uuid/"

        response = APIClient().delete(url)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_delete_genre_from_repository(
        self, genre_romance: Genre, genre_repository: DjangoORMGenreRepository
    ):
        genre_repository.save(genre_romance)

        assert genre_repository.get_by_id(genre_romance.id) is not None

        url = f"/api/genres/{genre_romance.id}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert genre_repository.get_by_id(genre_romance.id) is None
