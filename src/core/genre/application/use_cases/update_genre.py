from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)


class UpdateGenre:
    def __init__(
        self, repository: GenreRepository, category_repository: CategoryRepository
    ) -> None:
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        is_active: bool | None = None
        categories_id: set[UUID] | None = None

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID] = field(default_factory=set)

    def execute(self, input: Input) -> None:
        genre: Genre = self.repository.get_by_id(id=input.id)
        if genre is None:
            raise GenreNotFound(f"Genre with {input.id} not found")

        categories = self.category_repository.list()
        categories_id = {category.id for category in categories}
        if input.categories_id is not None and not input.categories_id.issubset(
            categories_id
        ):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.categories_id - categories_id}"
            )

        try:
            current_name = genre.name

            if input.name is not None:
                current_name = input.name

            genre.change_name(current_name)

            if input.is_active is True:
                genre.activate()

            if input.is_active is False:
                genre.deactivate()

            if input.categories_id is not None:
                genre.remove_all_categories()
                for category_id in input.categories_id:
                    genre.add_category(category_id)

        except ValueError as e:
            raise InvalidGenre(e)

        self.repository.update(genre)
        return self.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories,
        )
