from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    def __init__(
        self, repository: GenreRepository, category_repository: CategoryRepository
    ):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        is_active: bool = True
        categories_id: set[UUID] = field(default_factory=set)

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        categories = self.category_repository.list()
        categories_id = {category.id for category in categories}
        if not input.categories_id.issubset(categories_id):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.categories_id - categories_id}"
            )

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.categories_id,
            )
        except ValueError as e:
            raise InvalidGenre(e)

        self.repository.save(genre)
        return self.Output(id=genre.id)
