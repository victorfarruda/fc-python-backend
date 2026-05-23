from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.list_entity import output_entity
from src.core._shared.entity import ListOutputMeta
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
        current_page: int = 1
        per_page: int = 2

    @dataclass
    class Output:
        data: list[GenreOutput]
        meta: ListOutputMeta

    def execute(self, input: Input) -> Output:
        genres = self.repository.list()
        genres_list = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=sorted(genre.categories),
            )
            for genre in genres
        ]
        
        meta, paginated_genres = output_entity(input, genres_list)
        return self.Output(
            data=paginated_genres,
            meta=meta,
        )
