import uuid

import pytest

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestGetCategory:
    def test_get_category_by_id(self):
        category_filme = Category(name="Filme", description="Categoria para filmes")
        category_serie = Category(name="Série", description="Categoria para series")
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_filme.id)

        response: GetCategoryResponse = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_filme.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_filme = Category(name="Filme", description="Categoria para filmes")
        category_serie = Category(name="Série", description="Categoria para series")
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=uuid.uuid4())
        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
