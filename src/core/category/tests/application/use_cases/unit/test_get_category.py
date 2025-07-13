import uuid
from unittest.mock import create_autospec

import pytest

from core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_return_found_category(self):
        category = Category(
            name='Filme',
            description='Categoria para filmes',
            is_active=True,
        )
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.return_value = category

        use_case = GetCategory(repository=repository_mock)
        request = GetCategoryRequest(
            id=category.id
        )

        response: GetCategoryResponse = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name='Filme',
            description='Categoria para filmes',
            is_active=True,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.side_effect = CategoryNotFound()
        use_case = GetCategory(repository=repository_mock)
        request = GetCategoryRequest(
            id=uuid.uuid4()
        )
        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)
