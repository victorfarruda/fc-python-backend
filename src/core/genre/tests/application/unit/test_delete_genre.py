import uuid
from unittest.mock import create_autospec

import pytest

from core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.use_cases.delete_genre import (
    DeleteGenre,
)
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre import Genre


class TestDeleteGenre:
    def test_delete_genre_from_repository(self):
        genre = Genre(
            name="Filme",
        )
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = genre

        use_case = DeleteGenre(repository_mock)
        use_case.execute(DeleteGenre.DeleteGenreInput(id=genre.id))

        repository_mock.delete.assert_called_once_with(genre.id)

    def test_when_genre_not_found_then_raise_exception(self):
        repository_mock = create_autospec(GenreRepository)
        repository_mock.get_by_id.return_value = None
        use_case = DeleteGenre(repository=repository_mock)
        request = DeleteGenre.DeleteGenreInput(id=uuid.uuid4())
        with pytest.raises(GenreNotFound):
            use_case.execute(request)

        repository_mock.delete.assert_not_called()
