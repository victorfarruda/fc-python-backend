from dataclasses import dataclass
from uuid import UUID

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
        mapped_genres = sorted(
            [
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=sorted(genre.categories),
                )
                for genre in genres
            ],
            key=lambda g: getattr(g, input.order_by) if input.order_by else g.name,
        )

        page_offset = (input.current_page - 1) * input.per_page
        paginated_genres = mapped_genres[page_offset : page_offset + input.per_page]

        return self.Output(
            data=paginated_genres,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=input.per_page,
                total=len(mapped_genres),
            ),
        )
