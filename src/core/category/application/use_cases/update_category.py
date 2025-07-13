from dataclasses import dataclass
from uuid import UUID

from core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


@dataclass
class UpdateCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


class UpdateCategory:

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(id=request.id)
        if category is None:
            raise CategoryNotFound(f'Category with {request.id} not found')

        current_name = category.name
        current_description = category.description

        if request.name is not None:
            current_name = request.name

        if request.description is not None:
            current_description = request.description

        category.update_category(name=current_name, description=current_description)

        if request.is_active is True:
            category.activate()

        if request.is_active is False:
            category.deactivate()

        self.repository.update(category)
