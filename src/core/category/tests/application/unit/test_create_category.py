from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.application.exceptions import InvalidCategoryData


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository_mock = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=repository_mock)
        request = CreateCategoryRequest(
            name='Filme',
            description='Categoria para filmes',
            is_active=True,
        )

        response: CreateCategoryResponse = use_case.execute(request)

        assert isinstance(response, CreateCategoryResponse)
        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert repository_mock.save.called is True

    def test_create_category_with_invalid_data(self):
        repository_mock = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=repository_mock)
        request = CreateCategoryRequest(
            name='',
        )

        with pytest.raises(InvalidCategoryData, match='name cannot be empty') as exc_inf:
            use_case.execute(request)

        assert exc_inf.type is InvalidCategoryData
        assert str(exc_inf.value) == 'name cannot be empty'
