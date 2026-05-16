from uuid import UUID

import pytest

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

        response: CreateCategoryResponse = use_case.execute(request)

        assert isinstance(response, CreateCategoryResponse)
        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        assert repository.categories[0].id == response.id
        assert repository.categories[0].name == "Filme"
        assert repository.categories[0].description == "Categoria para filmes"
        assert repository.categories[0].is_active is True

    def test_create_category_with_invalid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="",
        )

        with pytest.raises(
            InvalidCategoryData, match="name cannot be empty"
        ) as exc_inf:
            use_case.execute(request)

        assert exc_inf.type is InvalidCategoryData
        assert str(exc_inf.value) == "name cannot be empty"
