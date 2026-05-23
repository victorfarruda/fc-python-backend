from dataclasses import dataclass, field
from uuid import UUID

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

        sorted_categories = sorted(
            [
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ],
            key=lambda x: getattr(x, request.order_by) if request.order_by else x.name,
        )

        page_offset = (request.current_page - 1) * request.per_page
        categories_page = sorted_categories[
            page_offset : page_offset + request.per_page
        ]

        return ListCategoryResponse(
            data=categories_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=request.per_page,
                total=len(sorted_categories),
            ),
        )
