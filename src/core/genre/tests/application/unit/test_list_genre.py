from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def movie_category() -> Category:
    fixed_uuid = uuid.UUID("23452678-1234-5678-1234-567812345678")
    return Category(id=fixed_uuid, name="Movie", description="Movie category")


@pytest.fixture
def documentary_category() -> Category:
    fixed_uuid = uuid.UUID("87654321-4321-8765-4321-876543218765")
    return Category(
        id=fixed_uuid, name="Documentary", description="Documentary movie category"
    )


@pytest.fixture
def drama_genre(movie_category, documentary_category) -> Genre:
    fixed_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
    return Genre(
        id=fixed_uuid,
        name="Drama",
        categories={movie_category.id, documentary_category.id},
    )


@pytest.fixture
def mock_genre_repository(drama_genre) -> GenreRepository:
    mock = create_autospec(GenreRepository)
    mock.list.return_value = [drama_genre]
    return mock


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = []
    return repository


class TestListGenre:
    def test_list_genre_with_associated_categories(
        self, drama_genre, mock_genre_repository, documentary_category, movie_category
    ):

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1

        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=drama_genre.id,
                    name=drama_genre.name,
                    is_active=drama_genre.is_active,
                    categories={movie_category.id, documentary_category.id},
                )
            ]
        )

    def test_list_genre_with_no_genres(self, mock_empty_genre_repository):
        use_case = ListGenre(repository=mock_empty_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
