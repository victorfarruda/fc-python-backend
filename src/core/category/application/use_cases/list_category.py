from dataclasses import dataclass, field
from uuid import UUID

from src.core._shared.application.list_entity import output_entity
from src.core._shared.entity import ListOutputMeta
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class ListCategoryRequest:
    order_by: str = ""
    current_page: int = 1
    per_page: int = 2


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()
        categories_list = [
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in categories
        ]

        meta, paginated_categories = output_entity(request, categories_list)
        return ListCategoryResponse(
            data=paginated_categories,
            meta=meta,
        )
