import pytest
from rest_framework.status import HTTP_200_OK
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
def category_repository(
    category_movie, category_documentary
) -> DjangoORMCategoryRepository:
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
