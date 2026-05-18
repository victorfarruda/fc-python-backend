from unittest.mock import create_autospec
import uuid
import re

import pytest

from core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.update_genre import (
    UpdateGenre,
)
from src.core.genre.domain.genre import Genre


class TestUpdateGenre:
    def test_update_genre_when_genre_does_not_exist(self):
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = None
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name="Comedy",
        )

        with pytest.raises(GenreNotFound, match=f"Genre with {input.id} not found"):
            use_case.execute(input)

    def test_update_genre_with_name_with_more_than_255_characters_should_raise_invalid_genre(
        self,
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="a" * 256,
        )
        with pytest.raises(InvalidGenre, match="name cannot be longer than 256"):
            use_case.execute(input)

        repository_mock.update.assert_not_called()

    def test_update_genre_with_empty_name_should_raise_invalid_genre(self):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="",
        )
        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(input)

        repository_mock.update.assert_not_called()

    def test_can_update_genre_name(self):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="Action",
        )

        use_case.execute(input)

        assert genre.name == "Action"
        repository_mock.update.assert_called_once_with(genre)

    def test_can_update_genre_name_and_is_active(self):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name="Action",
            is_active=False,
        )

        use_case.execute(input)

        assert genre.name == "Action"
        assert genre.is_active is False
        repository_mock.update.assert_called_once_with(genre)

    def test_can_update_genre_name_and_is_active_and_categories(self):
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
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = [
            documentary_category,
            movie_category,
        ]

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
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
        repository_mock.update.assert_called_once_with(genre)

    def test_update_genre_with_2_categories(self):
        documentary_category = Category(
            name="Documentary", is_active=True, description="Documentary category"
        )
        movie_category = Category(
            name="Movie", is_active=True, description="Movie category"
        )
        other_category = Category(
            name="Other", is_active=True, description="Other category"
        )
        genre = Genre(
            name="Comedy",
            is_active=True,
            categories={documentary_category.id, movie_category.id},
        )

        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = [
            documentary_category,
            movie_category,
            other_category,
        ]

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=genre.id,
            categories_id={other_category.id},
        )

        use_case.execute(input)

        assert genre.categories == input.categories_id

    def test_update_genre_with_non_existent_category_should_raise_related_categories_not_found(
        self,
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
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

        repository_mock.update.assert_not_called()

    def test_update_genre_with_non_existent_category_among_others_should_raise_related_categories_not_found(
        self,
    ):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = [
            Category(
                name="Documentary", is_active=True, description="Documentary category"
            )
        ]

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
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

        repository_mock.update.assert_not_called()

    def test_can_deactivate_genre(self):
        genre = Genre(
            name="Comedy",
            is_active=True,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=genre.id,
            is_active=False,
        )

        use_case.execute(input)

        assert genre.is_active is False
        assert genre.name == "Comedy"
        repository_mock.update.assert_called_once_with(genre)

    def test_can_activate_genre(self):
        genre = Genre(
            name="Comedy",
            is_active=False,
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre
        category_repository_mock = create_autospec(CategoryRepository)
        category_repository_mock.list.return_value = []

        use_case = UpdateGenre(
            repository=repository_mock, category_repository=category_repository_mock
        )
        input = UpdateGenre.Input(
            id=genre.id,
            is_active=True,
        )

        use_case.execute(input)

        assert genre.is_active is True
        assert genre.name == "Comedy"
        repository_mock.update.assert_called_once_with(genre)
