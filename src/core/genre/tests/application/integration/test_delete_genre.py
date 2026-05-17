import uuid

import pytest

from src.core.genre.application.use_cases.delete_genre import (
    DeleteGenre,
)
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository


class TestDeleteGenre:
    def test_delete_genre_from_repository(self):
        genre = Genre(
            name="Filme",
        )
        repository = InMemoryGenreRepository(genres=[genre])

        use_case = DeleteGenre(repository)
        use_case.execute(DeleteGenre.DeleteGenreInput(id=genre.id))

        assert repository.get_by_id(genre.id) is None
        assert len(repository.genres) == 0

    def test_when_genre_not_found_then_raise_exception(self):
        repository = InMemoryGenreRepository()
        request = DeleteGenre.DeleteGenreInput(id=uuid.uuid4())
        use_case = DeleteGenre(repository=repository)
        with pytest.raises(GenreNotFound):
            use_case.execute(request)

        assert len(repository.genres) == 0
