from dataclasses import dataclass
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = ""

    @dataclass
    class Output:
        data: list[GenreOutput]

    def execute(self, input: Input) -> Output:
        genres = self.repository.list()
        mapped_genres = sorted([
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=sorted(genre.categories),
            )
            for genre in genres
        ], key=lambda g: getattr(g, input.order_by) if input.order_by else g.name)

        return self.Output(data=mapped_genres)
