import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie", description="Movie category")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary", description="Documentary movie category")


@pytest.fixture
def category_repository(
    movie_category, documentary_category
) -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository(categories=[movie_category, documentary_category])


class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self, category_repository, documentary_category, movie_category
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            categories={category.id for category in category_repository.list()},
        )

        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre is not None
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_create_genre_with_non_existent_categories(self, category_repository):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        non_existent_category_id = uuid.uuid4()
        input = CreateGenre.Input(name="Action", categories={non_existent_category_id})

        with pytest.raises(RelatedCategoriesNotFound) as exec_info:
            use_case.execute(input)

        assert str(non_existent_category_id) in str(exec_info.value)

    def test_create_genre_without_categories(self, category_repository):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = CreateGenre.Input(name="Action", categories=set())

        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre is not None
        assert saved_genre.name == "Action"
        assert saved_genre.categories == set()
        assert saved_genre.is_active is True
