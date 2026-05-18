import uuid
import re

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.update_genre import (
    UpdateGenre,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository


@pytest.fixture
def genre_repository():
    return InMemoryGenreRepository()


@pytest.fixture
def category_repository():
    return InMemoryCategoryRepository()


class TestUpdateGenre:
    def test_update_genre_when_genre_does_not_exist(
        self, genre_repository, category_repository
    ):
        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name="Comedy",
        )

        with pytest.raises(GenreNotFound, match=f"Genre with {input.id} not found"):
            use_case.execute(input)

    def test_update_genre_with_name_with_more_than_255_characters_should_raise_invalid_genre(
        self, genre_repository, category_repository
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        genre_repository.save(genre)
        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="a" * 256,
        )
        with pytest.raises(InvalidGenre, match="name cannot be longer than 256"):
            use_case.execute(input)

    def test_update_genre_with_empty_name_should_raise_invalid_genre(
        self, genre_repository, category_repository
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        genre_repository.save(genre)
        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="",
        )
        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(input)

    def test_can_update_genre_name(self, genre_repository, category_repository):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        genre_repository.save(genre)
        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="Action",
        )

        use_case.execute(input)

        assert genre.name == "Action"

    def test_can_update_genre_name_and_is_active(
        self, genre_repository, category_repository
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        genre_repository.save(genre)
        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="Action",
            is_active=False,
        )

        use_case.execute(input)

        assert genre.name == "Action"
        assert genre.is_active is False

    def test_can_update_genre_name_and_is_active_and_categories(
        self, genre_repository, category_repository
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        documentary_category = Category(
            name="Documentary", is_active=True, description="Documentary category"
        )
        movie_category = Category(
            name="Movie", is_active=True, description="Movie category"
        )
        genre_repository.save(genre)
        category_repository.save(documentary_category)
        category_repository.save(movie_category)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="Action",
            is_active=False,
            categories_id={documentary_category.id, movie_category.id},
        )

        use_case.execute(input)

        assert genre.name == "Action"
        assert genre.is_active is False
        assert genre.categories == input.categories_id

    def test_update_genre_with_2_categories(
        self, genre_repository, category_repository
    ):
        documentary_category = Category(
            name="Documentary", is_active=True, description="Documentary category"
        )
        movie_category = Category(
            name="Movie", is_active=True, description="Movie category"
        )
        other_category = Category(
            name="Other", is_active=True, description="Other category"
        )
        category_repository.save(documentary_category)
        category_repository.save(movie_category)
        category_repository.save(other_category)

        genre = Genre(
            name="Comedy",
            is_active=True,
            categories={documentary_category.id, movie_category.id},
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            categories_id={other_category.id},
        )

        use_case.execute(input)

        assert genre.categories == input.categories_id

    def test_update_genre_with_non_existent_category_should_raise_related_categories_not_found(
        self, genre_repository, category_repository
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input: UpdateGenre.Input = UpdateGenre.Input(
            id=genre.id,
            categories_id={uuid.uuid4()},
        )

        with pytest.raises(
            RelatedCategoriesNotFound,
            match=re.escape(f"Categories not found: {input.categories_id}"),
        ):
            use_case.execute(input)

    def test_update_genre_with_non_existent_category_among_others_should_raise_related_categories_not_found(
        self, genre_repository, category_repository
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        genre_repository.save(genre)
        category_repository.save(
            Category(
                name="Documentary", is_active=True, description="Documentary category"
            )
        )

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        non_existent_category_id = uuid.uuid4()
        input: UpdateGenre.Input = UpdateGenre.Input(
            id=genre.id,
            categories_id={non_existent_category_id},
        )

        with pytest.raises(
            RelatedCategoriesNotFound,
            match=re.escape(f"Categories not found: {input.categories_id}"),
        ):
            use_case.execute(input)

    def test_can_deactivate_genre(self, genre_repository, category_repository):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            is_active=False,
        )

        use_case.execute(input)

        assert genre.is_active is False
        assert genre.name == "Comedy"

    def test_can_activate_genre(self, genre_repository, category_repository):
        genre = Genre(
            name="Comedy",
            is_active=False,
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            is_active=True,
        )

        use_case.execute(input)

        assert genre.is_active is True
        assert genre.name == "Comedy"
